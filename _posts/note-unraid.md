---
title: unRaid笔记
date: 2022-05-21 20:34:20
categories:
	- 笔记
tags:
	- unRaid
---

## 问题记录
### intel 12代集成显卡检测不出的问题`intel-gpu-top`

``` sh
echo "blacklist i915" > /boot/config/modprobe.d/i915.conf
# 开启核显
modprobe i915
# 显示 renderD128 就算成功了
ls /dev/dri
```

### 虚拟机直通显卡添加配置

> `<domain></domain>`标签中添加

``` xml
<qemu:commandline>
  <qemu:arg value='-set'/>
  <qemu:arg value='device.hostdev0.x-igd-opregion=on'/>
  <qemu:arg value='-set'/>
  <qemu:arg value='device.hostdev0.x-igd-gms=1'/>
 </qemu:commandline>
```

### 鼠标无法直通的问题
> 原本鼠标的配置是

``` xml
<hostdev mode='subsystem' type='usb'>
<source>
<vendor id='0x0000'/>
<product id='0x3825'/>
</source>
</hostdev>
```
> 在虚拟机中xml模式添加，bus和device的编号可以在：工具 -> 系统设备 中找到
``` xml
<hostdev mode='subsystem' type='usb' managed='yes'>
      <source>
        <address bus='11' device='2'/>
      </source>
    </hostdev>
```