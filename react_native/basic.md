# expo:
创建完 EAS 配置之后：
https://docs.expo.dev/get-started/set-up-your-environment/?mode=development-build
```powershell
eas build 
```
即可进行构建

# 示例工程的目录结构意义：
https://docs.expo.dev/get-started/start-developing/#having-problems

# 移除样板代码：
npm run reset-projectre

# our first program:
移除样板代码之后 这是我们的项目架构
```
PS D:\python\easy_phone_\easyphone> ls

    Directory: D:\python\easy_phone_\easyphone

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----           2025/8/14     1:06                .expo
d----           2025/8/13    17:06                .vscode
d----           2025/8/14    12:59                app
d----           2025/8/14    12:59                app-example
d----           2025/8/13    17:06                assets
d----           2025/8/14     0:34                node_modules
-a---          1985/10/26    16:15            411 .gitignore
-a---           2025/8/14     0:36           1104 app.json
-a---           2025/8/14     0:26            344 eas.json
-a---          1985/10/26    16:15            237 eslint.config.js
-a---           2025/8/14    13:00            110 expo-env.d.ts
-a---           2025/8/14     0:34         481945 package-lock.json
-a---           2025/8/14     0:34           1461 package.json
-a---          1985/10/26    16:15           1741 README.md
-a---           2025/8/13    17:19            262 tsconfig.json

```
app 内容：
```
PS D:\python\easy_phone_\easyphone> ls app

    Directory: D:\python\easy_phone_\easyphone\app

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---           2025/8/14    12:59             99 _layout.tsx
-a---           2025/8/14    13:03            468 index.tsx

```
_layout 特殊的布局文件
index 入口点
个人理解，二者赫尔外衣 变成普通工程的main.tsx
```

app 目录 ：一个特殊的目录，仅包含路由及其布局。添加到此目录的任何文件都会成为原生应用内的屏幕和 Web 页面上的页面。

根布局 ： app/_layout.tsx 文件。它定义共享的 UI 元素，例如标题和标签栏，以确保它们在不同的路由之间保持一致。

文件名约定 ： 索引文件名（例如 index.tsx ）与其父目录匹配，且不添加路径段。例如， app 目录中的 index.tsx 文件匹配 / 路由。（意思是index 不出现在url 中）

路由文件导出一个 React 组件作为其默认值。它可以使用 .js 、 .jsx 、 .ts 或 .tsx 扩展名。
Android, iOS, and web share a unified navigation structure.
Android、iOS 和 Web 共享统一的导航结构。

```
# _layout.tsx 维护主路由布局：
```tsx
import { Stack } from "expo-router";
import React from "react";

export default function RootLayout() {
  return (
  <>
  <Stack.Screen options={{ title: 'Oops! Not Found' }} />
    <Stack >
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="about" options={{ title: 'About' }} />
    </Stack>
  );
  </>
}


```
# 添加Link:
```tsx
export default function Index() {
  return (
    <View
      style={styles.container}
      >
      <Text style={styles.text}>Edit app/index.tsx to edit this screen.</Text>
      <Link href="/about">Go to about</Link>
    </View>
  );
}
```
# +not-found! 错误路由：
```tsx
import { View, StyleSheet } from 'react-native';
import { Link, Stack } from 'expo-router';

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: 'Oops! Not Found' }} />
      更改默认的标题
      <View style={styles.container}>
        <Link href="/" style={styles.button}>
          Go back to Home screen!
        </Link>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#25292e',
    justifyContent: 'center',
    alignItems: 'center',
  },

  button: {
    fontSize: 20,
    textDecorationLine: 'underline',
    color: '#fff',
  },
});


```
# tabs 底部栏
1. 调整文件架构
2. 修改父子路由：
```tsx
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="about" options={{ title: 'About' }} />
    </Tabs>
  );
}
```
```tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
}


```


# 反复用的view是div 的意思

# 接下来在 component 中添加 按钮 + 图像 。注意 使用的内置的组件 （来支持跨平台特性）
# 图像选择器代码
```tsx
import { Link } from "expo-router";
import React from "react";
import { Text, View,StyleSheet } from "react-native";
import ImageViewer from "@/component/ImageContainer";
import Button from "@/component/Button";
import * as ImagePicker from 'expo-image-picker';

const PlaceholderImage = require('@/assets/images/jietu.png');
export default function Index() {
    const pickImageAsync = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      console.log(result);
    } else {
      alert('You did not select any image.');
    }
  };
  return (
    <View
      style={styles.container}
      >
        <ImageViewer imgSource={PlaceholderImage} />
      <View style={styles.footerContainer}>
        <Button label="Choose a photo" theme="primary" />
        <Button label="Use this photo" />
      </View>
      <Text style={styles.text}>Edit app/index.tsx to edit this screen.</Text>
      <Link href="/about" style={styles.button}>Go to about</Link>

    </View>
  );
}
const styles = StyleSheet.create({
   container: {
    flex: 1,
    backgroundColor: '#25292e',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    color: '#fff',
  },
    button: {
    fontSize: 20,
    textDecorationLine: 'underline',
    color: '#fff',
  },
    footerContainer: {
    flex: 1 / 3,
    alignItems: 'center',
  },
})


```


# Modal : 一个突然出现的框制作
# flat list 滑动列表
# 动画制作：

首先动画值创建sharedValue
同时等待动画的组件要升级成animated 版本。
弄一个数学函数。
制作手势
制造useAniamgedValue动画
放入animagtd 组件
将组件放入手势检测器