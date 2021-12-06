---
title: Flutter Transporter上传ipa
date: 2021-12-06 23:51:58
tags:
  - iOS
---

> 在flutter项目中运行命令构建iOS文件

```
flutter build ios
```

> 生成存档

```
cd ios
xcodebuild -workspace Runner.xcworkspace -scheme Runner -sdk iphoneos -configuration Release archive -archivePath $PWD/build/Runner.xcarchive
```

> 添加配置文件`ExportOptions.plist`（需要在xcode上面选上自动管理签名），目录`MyProject/ios/ExportOptions.plist`

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>compileBitcode</key>
	<true/>
	<key>destination</key>
	<string>export</string>
	<key>method</key>
	<string>app-store</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>stripSwiftSymbols</key>
	<true/>
	<key>teamID</key>
	<string>填写你的teamID</string>
	 <key>uploadBitcode</key>
     <false/>
     <key>uploadSymbols</key>
     <false/>
</dict>
</plist>
```

> 生成ipa文件

```
xcodebuild -exportArchive -archivePath $PWD/build/Runner.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath $PWD/build/Runner.ipa
```

> 将`MyProject/ios/build/Runner.ipa`拖拽到Transporter点击发布


> 参考链接 [Publishing a Flutter app on Apple App store - Part 2](https://devbybit.com/publishing-a-flutter-app-on-apple-app-store-part-2/)

> 整理为一个运行的脚本文件一步搞定

{% codeblock pkg_ios.sh %}
rm -rf build/ios \
&& rm -rf ios/build \
&& flutter build ios \
&& cd ios \
&& xcodebuild -workspace Runner.xcworkspace -scheme Runner -sdk iphoneos -configuration Release archive -archivePath $PWD/build/Runner.xcarchive \
&& xcodebuild -exportArchive -archivePath $PWD/build/Runner.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath $PWD/build/Runner.ipa
{% endcodeblock %}
