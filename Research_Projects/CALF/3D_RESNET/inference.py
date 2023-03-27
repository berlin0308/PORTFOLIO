import time
import json
from collections import defaultdict
import cv2
import numpy
import statistics
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from utils import AverageMeter
import csv
from spatial_transforms import (Compose, Normalize, Resize, CenterCrop,
                                CornerCrop, MultiScaleCornerCrop,
                                RandomResizedCrop, RandomHorizontalFlip,
                                ToTensor, ScaleValue, ColorJitter,
                                PickFirstChannels)
import datetime


def get_video_results(outputs, class_names, output_topk):
    sorted_scores, locs = torch.topk(outputs,
                                     k=min(output_topk, len(class_names)))

    video_results = []
    for i in range(sorted_scores.size(0)):
        video_results.append({
            'label': class_names[locs[i].item()],
            'score': sorted_scores[i].item()
        })

    return video_results


def inference(data_loader, model, result_path, class_names, no_average,
              output_topk, time_feature=False):
    print('inference')

    model.eval()

    batch_time = AverageMeter()
    data_time = AverageMeter()
    results = {'results': defaultdict(list)}

    end_time = time.time()
    cont = 0
    with torch.no_grad():
        # with open('cows_data/results/results/feature_train_avgpool_ucf100001.tsv', 'a', newline='') as f_output:
        for i, (inputss, targets) in enumerate(data_loader):
            data_time.update(time.time() - end_time)

            video_ids, segments = zip(*targets)
            print(video_ids[0])
            inputs = inputss
            hour = inputss
            if time_feature:
                outputs = model(inputs, hour)
            else:
                outputs, feature_map = model(inputs)
            print(feature_map.size())
            outputs = F.softmax(outputs, dim=1).cpu()
            outing = torch.split(outputs, 1, 0)

            with open('cows_data/results/0210/results-layer2/val_avg_video'
                      '.tsv', 'a', newline='') as f_output:
                tsv_output = csv.writer(f_output, delimiter='\t')
                # tsv_output = csv.writer(f_output)
                class_label = video_ids[0].split('(', 1)[0]
                if class_label == 'auglame':
                    class_label = 'lame'

                if class_label == 'lame':
                    label = 0
                    class_label_neg = 'normal'

                elif class_label == 'normal':
                    label = 1
                    class_label_neg = 'lame'

                xi = []
                avg = []

                feature_len = len(torch.flatten(feature_map[0]).cpu().data.numpy().tolist())
                print(feature_len)

                for featur in range(feature_len):
                    avg.append(0)

                if i == 0:
                    for feature in range(feature_len):
                        ii = feature + 1
                        xi.append(str(ii))
                    xi.append(str(999))
                    tsv_output.writerow(xi)
                for scene in range(feature_map.size(0)):
                    a = torch.flatten(feature_map[scene]).cpu().data.numpy().tolist()  # 16
                    a.append(label)
                    # tsv_output.writerow(a)
                    for x in range(feature_len):
                        avg[x] += a[x]
                for x in range(feature_len):
                    avg[x] = avg[x] / feature_map.size(0)
                    # avg[x] = np.max(avg[x])
                avg.append(label)
                avg.append(video_ids[0])
                tsv_output.writerow(avg)
                avg.clear()

            for j in range(outputs.size(0)):
                results['results'][video_ids[j]].append({
                    'segment': segments[j],
                    'output': outputs[j]
                })
            # print(results['results'])
            batch_time.update(time.time() - end_time)
            end_time = time.time()

            print('[{}/{}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'.format(
                      i + 1,
                      len(data_loader),
                      batch_time=batch_time,
                      data_time=data_time))

    inference_results = {'results': {}}
    if not no_average:
        for video_id, video_results in results['results'].items():
            video_outputs = [
                segment_result['output'] for segment_result in video_results
            ]
            video_outputs = torch.stack(video_outputs)
            average_scores = torch.mean(video_outputs, dim=0)
            inference_results['results'][video_id] = get_video_results(
                average_scores, class_names, output_topk)
    else:
        for video_id, video_results in results['results'].items():
            inference_results['results'][video_id] = []
            for segment_result in video_results:
                segment = segment_result['segment']
                result = get_video_results(segment_result['output'],
                                           class_names, output_topk)
                inference_results['results'][video_id].append({
                    'segment': segment,
                    'result': result
                })

    with result_path.open('w') as f:
        json.dump(inference_results, f)


def get_normalize_method(mean, std, no_mean_norm, no_std_norm):
    if no_mean_norm:
        if no_std_norm:
            return Normalize([0, 0, 0], [1, 1, 1])
        else:
            return Normalize([0, 0, 0], std)
    else:
        if no_std_norm:
            return Normalize(mean, [1, 1, 1])
        else:
            return Normalize(mean, std)


def get_spatial_transform(opt, kind):
    normalize = get_normalize_method(opt.mean, opt.std, opt.no_mean_norm,
                                 opt.no_std_norm)
    if kind == "resnet":
        spatial_transform = [Resize(opt.sample_size)]
    else:
        spatial_transform = [Resize(opt.img_size)]
    if opt.inference_crop == 'center':
        spatial_transform.append(CenterCrop(opt.sample_size))
    spatial_transform.append(ToTensor())
    spatial_transform.extend([ScaleValue(opt.value_scale), normalize])
    spatial_transform = Compose(spatial_transform)
    return spatial_transform


def preprocessing(clip, spatial_transform):
    # Applying spatial transformations
    if spatial_transform is not None:
        spatial_transform.randomize_parameters()
        # Before applying spatial transformation you need to convert your frame into PIL Image format
        # (its not the best way, but works)
        clip = [spatial_transform(Image.fromarray(np.uint8(img)).convert('RGB')) for img in clip]
    # Rearange shapes to fit model input
    clip = torch.stack(clip, 0).permute(1, 0, 2, 3)
    clip = torch.stack((clip,), 0)
    return clip


def ipcam_main(opt, model):
    print("ipcam program running")
    full_clip = []
    classes = ['lame', 'normal']
    video_name = r'lame(26).mp4'
    cap = cv2.VideoCapture(r"cows_data/test_video/crop/" + video_name)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # out = cv2.VideoWriter(r"cows_data/test_video/results/" + video_name, fourcc, 30, (1920, 1080))
    out = cv2.VideoWriter(r"cows_data/test_video/crop/results/" + video_name, fourcc, 30, (800, 660))
    print("video opened")
    cc = 0
    startdate = datetime.datetime.today()
    print(startdate.strftime("%H"))
    lame = 0
    normal = 0
    with open('innovators1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        while True:
            # if int(startdate.strftime("%H")) >= 6 and int(startdate.strftime("%H")) < 17:
            if 1:
                if cc == 0:
                    cc += 1
                ret, image = cap.read()
                full_clip.append(image)
                if len(full_clip) > 16:
                    del full_clip[0]
                spatial_transform = get_spatial_transform(opt, "resnet")
                score, class_pred = ipcam_predict(full_clip, model, spatial_transform, classes)
                if class_pred == 'normal':
                    normal += 1
                elif class_pred == 'lame':
                    lame += 1
                print("lame: {}, normal: {}".format(lame, normal))
                if (lame+normal) != 0:
                    print("lame: {:5f}%".format(lame/(lame+normal)))
                    print("normal: {:5f}%".format(1-(lame/(lame+normal))))
                image = cv2.putText(image, class_pred + ": " + str(score), (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                    (255, 255, 255), 2, cv2.LINE_AA)
                # out.write(image)
                image = cv2.resize(image, (400, 300))
                cv2.imshow("cows", image)
                cv2.waitKey(1)


def ipcam_predict(clip, model, spatial_transform, classes):
    # Set mode eval mode
    model.eval()
    # do some preprocessing steps
    clip = preprocessing(clip, spatial_transform)
    # don't calculate grads
    with torch.no_grad():
        # apply model to input
        outputs = model(clip)
        # apply softmax and move from gpu to cpu
        outputs = F.softmax(outputs, dim=1).cpu()
        # get best class
        score, class_prediction = torch.max(outputs, 1)
        print("score: {}, class prediction: {}".format(score, classes[class_prediction]))
    # As model outputs a index class, if you have the real class list you can get the output class name
    # something like this: classes = ['jump', 'talk', 'walk', ...]
    if classes is not None:
        return score[0], classes[class_prediction[0]]
    return score[0], class_prediction[0]

