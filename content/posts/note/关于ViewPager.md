---
title: "关于ViewPager"
date: "2019-02-21"
description: "关于ViewPager"
featured : false
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---
## 关于ViewPager

使用方法：先在xml中定义

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
                                                 xmlns:tools="http://schemas.android.com/tools"
                                                 xmlns:app="http://schemas.android.com/apk/res-auto"
                                                 android:id="@+id/main_content"
                                                 android:layout_width="match_parent"
                                                 android:layout_height="match_parent"
                                                 android:fitsSystemWindows="true"
                                                 tools:context=".MainActivity">

    <android.support.v4.view.ViewPager
            android:background="@drawable/img5"
            android:id="@+id/view_pager"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layout_behavior="@string/appbar_scrolling_view_behavior"/>
</android.support.design.widget.CoordinatorLayout>
```

再到Activity中写

```java
package cn.euraxluo.myapplication;

import android.support.annotation.NonNull;
import android.support.v4.view.PagerAdapter;
import android.support.v7.app.AppCompatActivity;

import android.support.v4.view.ViewPager;
import android.os.Bundle;
import android.util.Log;
import android.view.*;

import android.widget.ImageView;
import cn.euraxluo.myapplication.transform.ZoomOutPageTransformer;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private ViewPager mViewPager;//viewpager
    private textViewAdapter mViewAdapter;
    private pictureViewAdapter mpViewAdapter;//图片的adapter
    private int[] mImage = new int[10];
    private View view1, view2, view3;
    private List<View> viewList = new ArrayList<View>(3);//view数组
    private LayoutInflater inflater;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
    }

    private void initView() {
        Log.d(TAG, "initView");
        mViewPager = (ViewPager) findViewById(R.id.view_pager);

        //关于图片的
//        initmImage();
//        mpViewAdapter = new pictureViewAdapter(mImage);
//        mViewPager.setAdapter(mpViewAdapter);
        //页面滑动
        initmlayouts();
        mViewAdapter = new textViewAdapter();
        mViewPager.setAdapter(mViewAdapter);
        mViewPager.setPageTransformer(true, new ZoomOutPageTransformer());//这一句是特效

    }

    private void initmImage() {
        mImage[0] = R.drawable.img1;
        mImage[1] = R.drawable.img2;
        mImage[2] = R.drawable.img3;
        mImage[3] = R.drawable.img4;
        mImage[4] = R.drawable.img5;
        mImage[5] = R.drawable.img6;

    }

    private void initmlayouts() {
        //findViewById是找具体的widget控件
        inflater = getLayoutInflater();//寻找xml下的布局文件，并且实例化
        view1 = (View) inflater.inflate(R.layout.activity_music, null);//这是三个layout
        view2 = (View) inflater.inflate(R.layout.activity_list, null);//实际用的时候发生了OOM
        view3 =  (View) inflater.inflate(R.layout.activity_about, null);

        viewList.add(view1);
        viewList.add(view2);
        viewList.add(view3);

    }

    public class pictureViewAdapter extends PagerAdapter {
        private int[] mImage;

        public pictureViewAdapter(int[] mImage) {
            this.mImage = mImage;//接受传入的mImge
        }

        @NonNull
        @Override
        public Object instantiateItem(@NonNull ViewGroup container, int position) {
            ImageView imageView = new ImageView(container.getContext());
            imageView.setImageResource(mImage[position]);//设置图片
            container.addView(imageView);
            return imageView;
        }

        @Override
        public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
            container.removeView((View) object);
        }

        @Override
        public int getCount() {//在viewpager显示几个页面
            return mImage.length;
        }

        @Override
        public boolean isViewFromObject(@NonNull View view, @NonNull Object o) {
            return view == o;
        }
    }

    public class textViewAdapter extends PagerAdapter {

        @Override
        public int getCount() {
            return viewList.size();//在viewPager中显示3个页面
        }

        @NonNull
        @Override
        public Object instantiateItem(@NonNull ViewGroup container, int position) {
            container.addView(viewList.get(position));//添加到viewPager容器中
            return viewList.get(position);//返回填充的对象
            //1.将当前视图添加到container中，2.返回当前View
        }

        @Override
        public boolean isViewFromObject(@NonNull View view, @NonNull Object o) {
            return view == o;
        }


        public void destroyItem(ViewGroup container, int position, Object obj) {
            container.removeView((View) obj);//从当前container删除指定位置的view
        }
    }
}

```

### 一些简单的特效

```java
package cn.euraxluo.myapplication.transform;
import android.support.v4.view.ViewPager;
import android.util.Log;
import android.view.View;

//扇子变换
public class RotateDownTransformer implements ViewPager.PageTransformer {
    private static final float ROT_MAX = 20.0f;
    private float mRot;


    public void transformPage(View view, float position)
    {
        Log.e("TAG", view + " , " + position + "");
        if (position < -1)
        { // [-Infinity,-1)
            // This page is way off-screen to the left.
            view.setRotation(0);
        } else if (position <= 1) // a页滑动至b页 ； a页从 0.0 ~ -1 ；b页从1 ~ 0.0
        { // [-1,1]
            // Modify the default slide transition to shrink the page as well
            if (position < 0)
            {
                mRot = (ROT_MAX * position);
                view.setPivotX(view.getMeasuredWidth() * 0.5f);
                view.setPivotY(view.getMeasuredHeight());
                view.setRotation( mRot);
            } else
            {
                mRot = (ROT_MAX * position);
                view.setPivotX(view.getMeasuredWidth() * 0.5f);
                view.setPivotY(view.getMeasuredHeight());
                view.setRotation( mRot);
            }
            // Scale the page down (between MIN_SCALE and 1)
            // Fade the page relative to its size.
        } else
        { // (1,+Infinity]
            // This page is way off-screen to the right.
            view.setRotation( 0);
        }
    }
}

```

```java
package cn.euraxluo.myapplication.transform;/* MyApplication2
 * cn.euraxluo.myapplication.Transform
 * ScalePageTransformer
 * 2019/5/18 16:31
 * author:Euraxluo
 * TODO
 */

import android.support.annotation.NonNull;
import android.support.v4.view.ViewPager;
import android.view.View;

public class ScalePageTransformer implements ViewPager.PageTransformer {
    private static final float MIN_SCALE=0.75f;

    @Override
    public void transformPage(@NonNull View page, float position) {
        if(position<-1.0f) {
            page.setScaleX(MIN_SCALE);
            page.setScaleY(MIN_SCALE);
        }
        // slide left
        else if(position<=0.0f) {
            page.setAlpha(1.0f);
            page.setTranslationX(0.0f);
            page.setScaleX(1.0f);
            page.setScaleY(1.0f);
        }
        // slide right
        else if(position<=1.0f) {
            page.setAlpha(1.0f-position);
            page.setTranslationX(-page.getWidth()*position);
            float scale=MIN_SCALE+(1.0f-MIN_SCALE)*(1.0f-position);
            page.setScaleX(scale);
            page.setScaleY(scale);
        }
        // out of right screen
        else {
            page.setScaleX(MIN_SCALE);
            page.setScaleY(MIN_SCALE);
        }
    }
}

```

```java
package cn.euraxluo.myapplication.transform;/* MyApplication2
 * cn.euraxluo.myapplication.Transform
 * ZoomOutPageTransformer
 * 2019/5/18 17:06
 * author:Euraxluo
 * TODO
 */


import android.annotation.SuppressLint;
import android.support.v4.view.ViewPager;
import android.view.View;

public class ZoomOutPageTransformer implements ViewPager.PageTransformer {
    private static final float MIN_SCALE = 0.85f;
    private static final float MIN_ALPHA = 0.85f;

    @SuppressLint("NewApi")
    public void transformPage(View view, float position) {
        if (position <= 1) //a页滑动至b页 ； a页从 0.0 -1 ；b页从1 ~ 0.0
        {// 还可以修改默认的幻灯片转换以缩小页面
            float scaleFactor = Math.max(MIN_SCALE, 1 - Math.abs(position));
            if (position < 0) {//代表左边的view
                view.setAlpha(1);
            } else {// 使页面相对于大小淡入颜色。
                view.setAlpha(MIN_ALPHA + (scaleFactor - MIN_SCALE)
                        / (2 - MIN_SCALE) * (2 - MIN_ALPHA));
            }
        }
    }

}
```

