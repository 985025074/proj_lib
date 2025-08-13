# gradle sync速度慢：
~~https://zhuanlan.zhihu.com/p/688998165~~
不要用上面那个 
下面这一个一劳永逸
明白了，你是想让 **Gradle 走你本机的 Windows 代理（127.0.0.1:端口号）**，这样就不会去访问 `mirrors.dormforce.net` 了。
Gradle 走代理需要在 `gradle.properties` 里设置，分两种位置都可以：

---

## **1. 全局配置（推荐）**

编辑：

* **Windows**

  ```
  C:\Users\<你的用户名>\.gradle\gradle.properties
  ```

如果没有这个文件，就新建一个。

写入（假设你的代理端口是 **7890**，你需要改成你的代理端口号）：

```properties
systemProp.http.proxyHost=127.0.0.1
systemProp.http.proxyPort=7890

systemProp.https.proxyHost=127.0.0.1
systemProp.https.proxyPort=7890
```

---

## **2. 项目级配置**

在项目根目录的 `gradle.properties` 文件里加同样的内容：

```properties
systemProp.http.proxyHost=127.0.0.1
systemProp.http.proxyPort=7890

systemProp.https.proxyHost=127.0.0.1
systemProp.https.proxyPort=7890
```

---

## **3. 关闭无效镜像源**

即使设置了代理，`mirrors.dormforce.net` 这个挂掉的源还是会拖慢下载，所以最好把 `build.gradle` 或 `settings.gradle` 里 `maven { url "https://mirrors.dormforce.net/..." }` 全部删掉或注释掉。

---

## **4. 测试**

保存配置 → 重新同步：

```bash
gradle --refresh-dependencies
```

或者在 Android Studio 里点击 **Sync Project with Gradle Files**。

---

你要不要我帮你**直接写一个带代理 + 国内备用源的完整 Gradle 配置**？
这样即使代理挂了也还能用阿里云继续下载。
# 卡在某个任务：
https://zhuanlan.zhihu.com/p/679195256


