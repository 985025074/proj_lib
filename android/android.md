# 第一份代码：
```kotlin
package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.ui.theme.MyApplicationTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyApplicationTheme {
        Greeting("An")
    }
}

```

@composable 表示component
@previde 最后会提供在现实之中

# 代码范式：
一个component  一个preview
# text 大小：
sp 缩放像素 ： dp 设备有关
# 尾随lambda：
有一些组件 包含需要(modifier = Modifier)=>{

}
# 与 网页不同。
不放在一个column 里 貌似都是position : absolute 。 相对于左上角进行布局
# box 上下对贴
# column 和 row 则是上下左右堆叠

各个布局的 情况：
https://developer.android.com/codelabs/basic-android-kotlin-compose-add-images?hl=zh-cn&continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-compose-unit-1-pathway-3%3Fhl%3Dzh-cn%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-compose-add-images#4

# 
帮我写一个kotlin android 程序。这个程序主要是为了说方言的老年人能够更方便的操控手机。
我已经做好语音识别的部分。由python 驱动语音识别的部分可以：传入录音音频。 分析出操作名
这个程序 由如下功能：
包含两个模块。一个模块是录音模块：录音模块中：
1. 可输入命令名 
2. 录制若干段音频。
另一模块为使用模块：
调用手机麦克风。录音，然后进行一系列动作。动作部分等下再说
