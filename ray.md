# 在 Python 中從 0 開始進行 *光線追踪*

> 全篇整理自 [Omar Aflak-Ray Tracing From Scratch in Python](https://omaraflak.medium.com/ray-tracing-from-scratch-in-python-41670e6a96f9)
> 
> 圖片、程式也來自上方出處，其他來源另標註

## 前言
讀完這篇文章將會了解電腦圖形演算法、光線追蹤演算法，並有一個簡單的 Python 實作，寫一個只要需 NumPy 的程式來生成下方圖片

![image](https://github.com/Jung217/alg112a/assets/99934895/f3021710-9f19-410d-8b2d-1364df24aa99)

## 先決條件
* 基本的向量幾何
* 如果有 2 個點 A 和 B (無論維數是多少：1、2、3、…、n)，可以透過計算找到從 A 到 B 的向量
* 向量的長度可以透過計算平方分量總和的平方根來找到。向量的長度 v 表示為 `||v||`
* 單位向量是長度為 1 的向量 (||v|| = 1)
* 給定一個向量，透過將第一個向量的每個分量除以其長度可以找到指向相同方向而長度為 1 的向量，稱為正歸化 (u = v / ||v||)
* 向量的點積 (<v, v> = ||v||²)
* 求解二次方程式

## 光追演算法
光線追蹤是一種模擬光路和與物體相交的渲染技術，能夠產生高度真實的影像。

* 設定一個場景：
  * 一個 3D 空間（使用 3 維座標在空間中定位物件）
  * 一些空間中的物體
  * 一個光源（一個向各個方向發射光的單點(一個點)）
  * 一隻「眼睛」 or 一台相機（觀察場景(一個點)）；
  * 一個螢幕 (因為相機可以觀察任何地方，相機將透過螢幕觀察物體（矩形螢幕的四個角落的 4 個位置）)
* 光追演算法
  ```
  對於螢幕的每個像素 p (x,y,z)：
      將黑色連結 p
      如果起始於相機的射線朝向 p 並與場景中的任何物件相交：
          計算最近物體交點
          如果射點和光之間沒有物體(相交)：
              計算交點顏色
              連結 p 的顏色交點
  ```
  ![image](https://github.com/Jung217/alg112a/assets/99934895/83b1653b-f906-4f0a-92ba-f902fc05ba9d)
  
> 這個過程實際上是現實中照明的相反過程；實際上，光線從光源向各個方向射出，在物體上反射並射入眼睛。
> 
> 但並非所有發出的光線都會進入眼睛，因此光線追蹤會執行**相反**的過程以**節省計算時間**

## 設定場景
在寫程式前，需要設定一個場景。為了達成目的，透過將它們與單位軸對齊來使事情變得簡單。相機位於 (0, 0, 1)，螢幕是 xy 平面的一部分。
```py
import numpy as np
import matplotlib.pyplot as plt

# 圖像寬高
width = 300
height = 200

# 相機位置
camera = np.array([0, 0, 1])

# 圖像寬高比
ratio = float(width) / height

# 螢幕邊界 (left, top, right, bottom)
screen = (-1, 1 / ratio, 1, -1 / ratio)

# 初始化圖像數據
image = np.zeros((height, width, 3))

# 迭代每個像素
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # 在這裡填入根據需求設置像素顏色的程式碼
        # image[i, j] = ...

        # 顯示進度
        print("progress: %d/%d" % (i + 1, height))

# 將圖像保存為 PNG 檔案
plt.imsave('image.png', image)
```

## 射線相交
### 射線定義
> 射線實際上該說是向量。當編寫幾何圖形時，應該使用向量，它們更容易使用，並且更不容易出現除零等錯誤。
由於光線從相機開始並向當前目標像素的方向前進，因此我們可以定義一個指向相似方向的單位向量。

將「從相機開始朝向像素的光線」定義為以下等式：

![image](https://github.com/Jung217/alg112a/assets/99934895/47455479-5f7e-4be0-a98c-9ef54a5f3b77)

**相機和像素都是 3D 點**。因為 t=0 最終會到相機的位置，並且增加的越多，在像素方向上 t 與相機的距離就越遠。
這個參數函式對於給定的 t 產生沿直線的點。(定義一條從原點（O）開始並朝向目的地（D）的射線，d 定義為方向向量)：

![image](https://github.com/Jung217/alg112a/assets/99934895/27f42986-1c6d-4573-81ab-abda13ce246e)

(添加 origin 和 direction 的計算，兩者定義了一條射線。像素的 z=0，因為它在螢幕上 (螢幕在 xy平面中))
```py
import numpy as np
import matplotlib.pyplot as plt

# 正規化向量(單位向量)
def normalize(vector):
    return vector / np.linalg.norm(vector)

# 圖像寬高
width = 300
height = 200

# 相機位置
camera = np.array([0, 0, 1])

# 圖像寬高比
ratio = float(width) / height

# 螢幕邊界 (left, top, right, bottom)
screen = (-1, 1 / ratio, 1, -1 / ratio)

# 初始化圖像數據
image = np.zeros((height, width, 3))

# 迭代每個像素
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # 當前像素的三維坐標
        pixel = np.array([x, y, 0])

        # 相機到像素的方向向量（歸一化）
        origin = camera
        direction = normalize(pixel - origin)

        # 在這裡填入根據需求設置像素顏色的程式碼
        # image[i, j] = ...

    # 顯示進度
    print("progress: %d/%d" % (i + 1, height))

# 將圖像保存為 PNG 檔案
plt.imsave('image.png', image)
```

### 球體定義
> 球體其實是一個定義起來非常簡單的物件。球體被定義為距中心點的距離 r（半徑）相同的點的集合。

給定球體的中心C及其半徑r，任意點X位於球體上若且唯若：

![image](https://github.com/Jung217/alg112a/assets/99934895/60a446e1-0c2b-482e-9638-6f94f9a93124)

為了方便，將兩邊平方，以消除由 X — C 的大小引起的平方根

![image](https://github.com/Jung217/alg112a/assets/99934895/4950239c-7cd4-4d7f-a157-6cb62f1bdda9)

```py
# 定義一些球體物件
objects = [
    { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7 },
    { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1 },
    { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15 }
]
```

### 球體交點
我們知道射線函式，也知道一個點必須滿足什麼條件才能位於球體上。

現在所要做的就是插入 `eq. 2` 並 `eq. 4` 求解 `t` 這意代表：哪些 t、ray(t) 位於球體上

![image](https://github.com/Jung217/alg112a/assets/99934895/e9508b57-d432-42fa-9b89-d8b99b09b684)

這是可以求解的普通二次方程式 t。t², t¹, t⁰ 將分別呼叫與 a、b 和 c 相關的係數。計算方程式的判別式：

![image](https://github.com/Jung217/alg112a/assets/99934895/baee7a61-e4d1-4662-807d-a8f97a839025)

由於 d（方向）是單位向量，因此我們有 a=1。一旦計算出方程式的判別式，就有 3 種可能性：

![image](https://github.com/Jung217/alg112a/assets/99934895/ab4999e5-00fe-4a13-b58f-8bb4ecc90f7f)

這裡只會使用**第三種**情況來偵測交叉點。這是一個可以偵測射線和球體之間相交的函數。如果射線與球體相交，它將從射線返原點回到最近交點 t 的距離，否則返回 None。

(僅當 t1 和 t2 均為正數時，才會傳回最近的交集。因為求解方程式的 a 可能為負，這意味著與球體相交的光線沒有 d 作為方向向量，而是-d（E.g.球體位於相機和螢幕後面）)

```py
# 相交判斷
def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None
```

### 最近相交對象
可以建立一個函數，用於 `sphere_intersect()` 尋找光線相交的最近的物件。只需遍歷所有球體，搜尋交叉點，並保留最近的球體。

呼叫函數時，如果 `nearest_object` 是 **None** 則表示沒有與射線相交的物體，否則其值為最近的相交物體從射線原點到交點 `min_distance` 的距離。

```py
# 最近相交判斷
def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None
```

### 交點
為了計算交點，使用前面的函數
```
nearest_object, distance = nearest_intersected_object(objects, o, d)
if nearest_object:
    intersection_point = o + d * distance
```

### 光交點
想知道從相交點開始並向光發出的光線在穿過光之前是否與場景中的物體相交，這只需要更改光線原點和方向。

首先，需要定義一盞燈(光源)：
```
light = { 'position': np.array([5, 5, 5]) }
```
要檢查物體是否遮擋交點，必須傳遞從交點開始並向光源發出的光線，查看返回的最近物體是否實際上比光源更接近交點（介於兩者之間）。
(如果使用交點作為新光線的原點，最終可能會偵測到目前所在球體作為交點和光線之間的物件。解決問題的一個快速且廣泛使用的解決方案是採取一小步，讓我們遠離球體表面。通常使用表面的法線向量並朝該方向邁出一小步。(適用於任何物體))

![image](https://github.com/Jung217/alg112a/assets/99934895/3e0105f7-5ac8-4988-a2b0-16c48996511f)

```py
# ...
intersection = origin + min_distance * direction

normal_to_surface = normalize(intersection - nearest_object['center'])
shifted_point = intersection + 1e-5 * normal_to_surface
intersection_to_light = normalize(light['position'] - shifted_point)

_, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light)
intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
is_shadowed = min_distance < intersection_to_light_distance

if is_shadowed:
    continue
```

## Blinn-Phong 反射模型
我們知道光束照射到物體上，光束的反射直接進入相機。但相機看到了什麼？這就是 Blinn-Phong 模型解決的問題。

Blinn-Phong 模型是計算強度較小的 [Phong 模型](https://en.wikipedia.org/wiki/Phong_reflection_model)

在模型中，所有物體具備以下四個屬性 (所有顏色都是0–1範圍內的RGB表示形式) :
* 環境顏色 (Ambient color) : 物體在沒有光的情況下應該有的顏色
* 漫反射顏色 (Diffuse color) : 最接近平常所說的「顏色」的顏色
* 鏡面顏色 (Specular color) : 線照射到物體上時，物體發光部分的顏色 (大多是白色)
* 閃亮系數 (Shininess) : 表示物體光澤程度的係數

![image](https://github.com/Jung217/alg112a/assets/99934895/975e539b-a01f-45ab-983f-e6b523229aec)
```py
objects = [
    { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100 },
    { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100 },
    { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100 }
]
```
在 Blinn-Phong 模型中，**光**還具有三種屬性：環境光、漫反射和鏡面反射。
```py
light = { 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }
```
Blinn-Phong 模型計算點的光照如下：

![image](https://github.com/Jung217/alg112a/assets/99934895/970d57ee-74b9-4665-aa58-4d968387b144)

* ka, kd, ks 是物體的環境光、漫反射、鏡面反射屬性
* ia, id, is 是光的環境光、漫反射、鏡面反射屬性
* L 是從交點到光方向的單位向量
* N 是交點處物體表面的單位法向量
* V 是從交點到相機方向的單位向量
* α 是物體的光澤度

```py
# ...
if is_shadowed:
    break

# RGB
illumination = np.zeros((3))

# 環境
illumination += nearest_object['ambient'] * light['ambient']

# 漫反射
illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

# 鏡面
intersection_to_camera = normalize(camera - intersection)
H = normalize(intersection_to_light + intersection_to_camera)
illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)

image[i, j] = np.clip(illumination, 0, 1)
```

## RUN THE CODE !!
增加寬度和高度以得到更高的解析度（解析度越高，時間越久）。

![image](https://github.com/Jung217/alg112a/assets/99934895/02855d96-0487-4df2-9ade-5a7b953a62ce)

與第一張圖比，**少了灰色地板**，**且無反射效果**

## 假平面
理想情況下，我們會創建另平面，但也可以簡單地使用另一個球體。如果你站在一個半徑無限大（與你的尺寸相比）的球體上，那麼你會感覺就像站在平坦的表面上。就像地球一樣。
```py
{ 'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100 }
```

## 反射
目前 : 從光源發出，撞擊物體的表面，然後直接彈向相機。

如果光線在撞擊相機之前撞擊了多個物體怎麼辦？ >>> **光線會累積不同的顏色，當它回到相機時，就會看到反射**。

每個物體的反射係數在 0–1 範圍內。「0」表示物體無光澤，「1」表示物體像鏡子。
```py
{ 'center': np.array([-0.2, 0, -1]), ..., 'reflection': 0.5 } 
{ 'center': np.array([0.1, -0.3, 0]), . .., 'reflection': 0.5 } 
{ 'center': np.array([-0.3, 0, 0]), ..., 'reflection': 0.5 } 
{ 'center': np.array([0, -9000, 0]), ..., 'reflection': 0.5 }
```
### 演算法
目前 : 計算一條從相機開始並向像素移動的光線，然後將光線追蹤到場景中，檢查最近的交點併計算交點顏色。

為了包含反射，需要在相交發生後追蹤反射光線並包含每個相交點的顏色貢獻。重複該過程特定次數
### 顏色計算
為了得到像素的顏色，我們需要將光線對每個相交點的貢獻求和。

![image](https://github.com/Jung217/alg112a/assets/99934895/2391ec70-675f-4a49-8d76-4f5b11d625cf)
* c 是像素的（最終）顏色
* i 是 #index 交點的 Blinn-Phong 模型計算的光照
* r 是 #index 相交對象的反射

自行決定何時停止計算總和（停止追蹤反射光線）
### 反射光線
在對此進行寫程式前，需要找到反射光線的方向。可以透過以下方式計​​算反射的光線：

![image](https://github.com/Jung217/alg112a/assets/99934895/883a2f8d-5723-48a2-b905-257c4c81b687)
![image](https://github.com/Jung217/alg112a/assets/99934895/32125564-2690-4fb7-a856-a9e98c443dd1)
* R 是正歸化的反射光線
* V 為被反射光線方向的單位向量
* N 是射線筆畫表面法向的單位向量

將此方法與函數一起添加到程式上方的 `normalize()`
```py
def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis
```
</br>

> 這是最後的一個小改變。只需進行以下更改：
```py
# 全域變數以及圖像寬高等相關參數
max_depth = 3

# 迴圈開始，迭代每個像素
for k in range(max_depth):
    # 找到最近的物體和距離
    nearest_object, min_distance = find_nearest_object(origin, direction)

    # 計算光照
    illumination = calculate_illumination(nearest_object, origin, direction)

    # 反射部分
    color += reflection * illumination
    reflection *= nearest_object['reflection']

    # 計算新的射線起點和方向
    origin = shifted_point
    direction = reflected(direction, normal_to_surface)

# 設置像素的顏色，並進行範圍限制
image[i, j] = np.clip(color, 0, 1)
```

## 最終的程式 & 結果
![image](https://github.com/Jung217/alg112a/assets/99934895/d6303e82-9416-4f4b-8769-63745e2e9b1a)
```py
import numpy as np
import matplotlib.pyplot as plt

# 函數：將向量歸一化
def normalize(vector):
    return vector / np.linalg.norm(vector)

# 函數：計算反射向量
def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

# 函數：球體相交測試
def sphere_intersect(center, radius, ray_origin, ray_direction):
    # 球體相交方程
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c

    # 檢查相交點
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

# 函數：找到最近的相交物體
def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [sphere_intersect(obj['center'], obj['radius'], ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance

# 設置相機和畫面大小等相關參數
width = 300
height = 200

max_depth = 3

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

# 光源參數
light = {'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]),
         'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1])}

# 物體列表
objects = [
    {'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]),
     'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]),
     'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]),
     'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]),
     'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5}
]

# 生成空白畫布
image = np.zeros((height, width, 3))

# 迭代每個像素
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # 創建像素光線
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        color = np.zeros((3))
        reflection = 1

        # 迭代光線
        for k in range(max_depth):
            # 檢查相交物體
            nearest_object, min_distance = nearest_intersected_object(objects, origin, direction)
            if nearest_object is None:
                break

            intersection = origin + min_distance * direction
            normal_to_surface = normalize(intersection - nearest_object['center'])
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = normalize(light['position'] - shifted_point)

            _, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light)
            intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                break

            illumination = np.zeros((3))

            # 環境光
            illumination += nearest_object['ambient'] * light['ambient']

            # 漫反射
            illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

            # 鏡面反射
            intersection_to_camera = normalize(camera - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (
                        nearest_object['shininess'] / 4)

            # 反射
            color += reflection * illumination
            reflection *= nearest_object['reflection']

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

        # 將顏色值應用於畫素，並進行範圍限制
        image[i, j] = np.clip(color, 0, 1)
    print("%d/%d" % (i + 1, height))

# 保存生成的圖像
plt.imsave('image.png', image)
```

