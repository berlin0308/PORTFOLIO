import torch
import time
import sys
import csv
import torch
import torch.distributed as dist
import numpy as np
from utils import AverageMeter, calculate_accuracy,calculate_precision_and_recall
from sklearn.metrics import confusion_matrix,plot_confusion_matrix
import matplotlib.pyplot as plt


def val_epoch(epoch,
              data_loader,
              model,
              criterion,
              device,
              logger,
              tb_writer=None,
              distributed=False,
              time_feature=False):
    print('validation at epoch {}'.format(epoch))

    model.eval()

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    accuracies = AverageMeter()

    end_time = time.time()

    with torch.no_grad():
        with open('cows_data/features map.tsv', 'w', newline='') as f_output:
            for i, (inputss, targets) in enumerate(data_loader):
                # print(targets)
                data_time.update(time.time() - end_time)
                inputs = inputss
                hour = inputss
                targets = targets.to(device, non_blocking=True)
                if time_feature:
                    outputs = model(inputs, hour)
                else:
                    # outputs = model(inputs)
                    outputs, feature_map = model(inputs)
                    print(type(feature_map))
                    tsv_output = csv.writer(f_output)
                    tsv_output.writerow(torch.flatten(feature_map).cpu().data.numpy())
                    tsv_output.writerow(targets)
                    tsv_output.writerow(" ")
                    # print(feature_map)

                pred = outputs.cpu().data.numpy().argmax(axis=1)
                truth = targets.cpu().data.numpy()

                loss = criterion(outputs, targets)
                acc = calculate_accuracy(outputs, targets)
                # prec,recall,fscore=calculate_precision_and_recall(outputs,targets,1)

                losses.update(loss.item(), inputs.size(0))
                accuracies.update(acc, inputs.size(0))

                batch_time.update(time.time() - end_time)
                end_time = time.time()

                print('Epoch: [{0}][{1}/{2}]\t'
                      'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                      'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                      'Acc {acc.val:.3f} ({acc.avg:.3f})'.format(
                          epoch,
                          i + 1,
                          len(data_loader),
                          batch_time=batch_time,
                          data_time=data_time,
                          loss=losses,
                          acc=accuracies))

    if distributed:
        loss_sum = torch.tensor([losses.sum],
                                dtype=torch.float32,
                                device=device)
        loss_count = torch.tensor([losses.count],
                                  dtype=torch.float32,
                                  device=device)
        acc_sum = torch.tensor([accuracies.sum],
                               dtype=torch.float32,
                               device=device)
        acc_count = torch.tensor([accuracies.count],
                                 dtype=torch.float32,
                                 device=device)

        dist.all_reduce(loss_sum, op=dist.ReduceOp.SUM)
        dist.all_reduce(loss_count, op=dist.ReduceOp.SUM)
        dist.all_reduce(acc_sum, op=dist.ReduceOp.SUM)
        dist.all_reduce(acc_count, op=dist.ReduceOp.SUM)

        losses.avg = loss_sum.item() / loss_count.item()
        accuracies.avg = acc_sum.item() / acc_count.item()

    if logger is not None:
        logger.log({'epoch': epoch, 'loss': losses.avg, 'acc': accuracies.avg})

    if tb_writer is not None:
        tb_writer.add_scalar('val/loss', losses.avg, epoch)
        tb_writer.add_scalar('val/acc', accuracies.avg, epoch)

    return losses.avg
