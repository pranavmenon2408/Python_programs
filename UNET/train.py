import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from model import UNET
from utils import (
    load_checkpoint,
    save_checkpoint,
    get_loaders,
    check_accuracy,
    
)

LR=1e-4
device="cuda" if torch.cuda.is_available() else "cpu"
batch_size=16
num_epochs=3
num_workers=2
img_height=160
img_width=240
pin_memory=True
load_model=False
train_img_dir="data/train"
train_mask_dir="data/train_masks"
val_img_dir="data/val"
val_mask_dir="data/val_masks"

def train_fn(loader,model,optimizer,loss_fn,scaler):
    loop=tqdm(loader)
    for batch_idx, (data,targets) in enumerate(loop):
        data=data.to(device=device)
        targets=targets.float().unsqueeze(1).to(device=device)

        predictions=model(data)
        loss=loss_fn(predictions,targets)

        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        loop.set_postfix(loss=loss.item())

def main():
    train_transform=A.Compose([
        A.Resize(height=img_height,width=img_width),
        A.Rotate(limit=35,p=1.0),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.1),
        A.Normalize(
            mean=[0.0,0.0,0.0],
            std=[1.0,1.0,1.0],
            max_pixel_value=255.0
        ),
        ToTensorV2(),
    ],)

    val_transform=A.Compose([
        A.Resize(height=img_height,width=img_width),
        A.Normalize(mean=[0.0,0.0,0.0],
            std=[1.0,1.0,1.0],
            max_pixel_value=255.0),
            ToTensorV2(),
    ],)

    model=UNET(in_channels=3,out_channels=1).to(device=device)
    loss_fn=nn.BCEWithLogitsLoss()
    optimizer=optim.Adam(model.parameters(),lr=LR)

    train_loader,val_loader=get_loaders(
        train_img_dir,train_mask_dir,val_img_dir,val_mask_dir,batch_size,train_transform,val_transform,num_workers,pin_memory
    )

    scaler=torch.cpu.amp.grad_scaler.GradScaler()
    for epoch in range(num_epochs):
        train_fn(train_loader,model,optimizer,loss_fn,scaler)

        checkpoint={"state_dict":model.state_dict(),
                    "optimizer":optimizer.state_dict()}
        
        save_checkpoint(checkpoint)
        check_accuracy((val_loader,model,device))



if __name__=="__main__":
    main()