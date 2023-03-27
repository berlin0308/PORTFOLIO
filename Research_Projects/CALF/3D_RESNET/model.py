import torch
from torch import nn

from models import resnet, resnet2p1d, pre_act_resnet, wide_resnet, resnext, densenet


def get_module_name(name):
    name = name.split('.')
    if name[0] == 'module':
        i = 1
    else:
        i = 0
    if name[i] == 'cnn':
        i += 1
    if name[i] == 'features':
        i += 1
    # if name[i] == 'layer4':
    #   return name[i+1]

    return name[i]


def get_fine_tuning_parameters(model, ft_begin_module):
    if not ft_begin_module:
        return model.parameters()

    parameters = []
    add_flag = False
    for k, v in model.named_parameters():
        print(k)
        if ft_begin_module == get_module_name(k):
            add_flag = True

        if add_flag:
            parameters.append({'params': v})

    return parameters


def generate_model(opt):
    assert opt.svm in [
        'resnet', 'resnet2p1d', 'preresnet', 'wideresnet', 'resnext', 'densenet'
    ]

    if opt.svm == 'resnet':
        model = resnet.generate_model(model_depth=opt.model_depth,
                                      n_classes=opt.n_classes,
                                      n_input_channels=opt.n_input_channels,
                                      shortcut_type=opt.resnet_shortcut,
                                      conv1_t_size=opt.conv1_t_size,
                                      conv1_t_stride=opt.conv1_t_stride,
                                      no_max_pool=opt.no_max_pool,
                                      widen_factor=opt.resnet_widen_factor)
    elif opt.svm == 'resnet2p1d':
        model = resnet2p1d.generate_model(model_depth=opt.model_depth,
                                          n_classes=opt.n_classes,
                                          n_input_channels=opt.n_input_channels,
                                          shortcut_type=opt.resnet_shortcut,
                                          conv1_t_size=opt.conv1_t_size,
                                          conv1_t_stride=opt.conv1_t_stride,
                                          no_max_pool=opt.no_max_pool,
                                          widen_factor=opt.resnet_widen_factor)
    elif opt.svm == 'wideresnet':
        model = wide_resnet.generate_model(
            model_depth=opt.model_depth,
            k=opt.wide_resnet_k,
            n_classes=opt.n_classes,
            n_input_channels=opt.n_input_channels,
            shortcut_type=opt.resnet_shortcut,
            conv1_t_size=opt.conv1_t_size,
            conv1_t_stride=opt.conv1_t_stride,
            no_max_pool=opt.no_max_pool)
    elif opt.svm == 'resnext':
        model = resnext.generate_model(model_depth=opt.model_depth,
                                       cardinality=opt.resnext_cardinality,
                                       n_classes=opt.n_classes,
                                       n_input_channels=opt.n_input_channels,
                                       shortcut_type=opt.resnet_shortcut,
                                       conv1_t_size=opt.conv1_t_size,
                                       conv1_t_stride=opt.conv1_t_stride,
                                       no_max_pool=opt.no_max_pool)
    elif opt.svm == 'preresnet':
        model = pre_act_resnet.generate_model(
            model_depth=opt.model_depth,
            n_classes=opt.n_classes,
            n_input_channels=opt.n_input_channels,
            shortcut_type=opt.resnet_shortcut,
            conv1_t_size=opt.conv1_t_size,
            conv1_t_stride=opt.conv1_t_stride,
            no_max_pool=opt.no_max_pool)
    elif opt.svm == 'densenet':
        model = densenet.generate_model(model_depth=opt.model_depth,
                                        n_classes=opt.n_classes,
                                        n_input_channels=opt.n_input_channels,
                                        conv1_t_size=opt.conv1_t_size,
                                        conv1_t_stride=opt.conv1_t_stride,
                                        no_max_pool=opt.no_max_pool)

    return model


def load_pretrained_model(model, pretrain_path, model_name, n_finetune_classes, time_feature=False):
    if pretrain_path:
        print('loading pretrained model {}'.format(pretrain_path))
        pretrain = torch.load(pretrain_path, map_location='cpu')

        model.load_state_dict(pretrain['state_dict'])
        tmp_model = model
        if time_feature:
            class MyModel(nn.Module):
                def __init__(self):
                    super(MyModel, self).__init__()
                    self.cnn = tmp_model
                    self.cnn.fc = nn.Linear(self.cnn.fc.in_features, 7)  # 把feature減少成7個 不然2個time feature會被稀釋掉
                    self.fc1 = nn.Linear(7+2, n_finetune_classes)

                def forward(self, x, t):
                    x1 = self.cnn(x)
                    x2 = t
                    x3 = torch.cat((x1, x2), 1)
                    out = self.fc1(x3)
                    return out
            model = MyModel()
        else:

            class featureModel(nn.Module):
                def __init__(self):
                    super(featureModel, self).__init__()
                    self.cnn = tmp_model              # in feature=512     # 這裡就是把原本的model繼承到自定義的模型
                    self.cnn.fc = nn.Linear(tmp_model.fc.in_features, n_finetune_classes)

                def forward(self, x):
                    x = self.cnn.conv1_s(x)
                    x = self.cnn.bn1_s(x)
                    x = self.cnn.conv1_t(x)
                    x = self.cnn.bn1_t(x)
                    x = self.cnn.relu(x)
                    x = self.cnn.maxpool(x)
                    x = self.cnn.layer1(x)
                    x = self.cnn.layer2(x)
                    x = self.cnn.layer3(x)
                    x = self.cnn.layer4(x)
                    x = self.cnn.avgpool(x)
                    feature_map = x
                    x = x.view(x.size(0), -1)
                    out = self.cnn.fc(x)
                    # out = self.cnn(x)                     # 做 feature extraction
                    return out, feature_map

            model = featureModel()
            # tmp_model.fc = nn.Linear(tmp_model.fc.in_features, n_finetune_classes)
        # tmp_model.fc = nn.Sequential(nn.Linear(tmp_model.fc.in_features,10),nn.Linear(10,n_finetune_classes))

    return model


def make_data_parallel(model, is_distributed, device):
    if is_distributed:
        if device.type == 'cuda' and device.index is not None:
            torch.cuda.set_device(device)
            model.to(device)

            model = nn.parallel.DistributedDataParallel(model,
                                                        device_ids=[device])
        else:
            model.to(device)
            model = nn.parallel.DistributedDataParallel(model)
    elif device.type == 'cuda':
        model = nn.DataParallel(model, device_ids=None).cuda()

    return model
