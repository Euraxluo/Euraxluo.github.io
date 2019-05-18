## 关于musicplayer



### 首先给权限

```xml
	<!-- 网络权限 -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <!-- 向SD卡写入数据权限 -->
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <!-- 在SD卡中创建与删除文件权限 -->
	<!-- 扫描数据库的权限 -->
    <uses-permission 
            android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS"
            tools:ignore="ProtectedPermissions"/>
```



包含ListView的布局文件

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
        xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:tools="http://schemas.android.com/tools"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:layout_gravity="center"
        tools:context=".MainActivity">

    <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="400dp"
            android:orientation="vertical">

        <ListView
                android:id="@+id/lv1"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"></ListView>
    </LinearLayout>


    <SeekBar
            android:id="@+id/sb"
            android:layout_width="match_parent"
            android:layout_height="30dp"
            android:maxHeight="2dp"
            android:minHeight="2dp"
            android:paddingBottom="3dp"
            android:paddingLeft="12dp"
            android:max="200"
            android:paddingRight="12dp"
            android:paddingTop="3dp" />
    <TextView
            android:id="@+id/tv1"
            android:layout_width="match_parent"
            android:layout_height="wrap_content" />

    <LinearLayout
            android:orientation="horizontal"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content">
        <cn.study.euraxluo.androidtup.CircleImageView
                android:id="@+id/imageView"
                android:layout_width="70dp"
                android:layout_height="70dp"
                android:scaleType="centerCrop"
                />
        <Button
                android:id="@+id/btn_last"
                android:layout_width="70dp"
                android:layout_height="wrap_content"
                android:text="@string/btn_last"/>
        <Button
                android:id="@+id/btn_star"
                android:layout_width="70dp"
                android:layout_height="wrap_content"
                android:text="@string/btn_star"/>
        <Button
                android:id="@+id/btn_next"
                android:layout_width="70dp"
                android:layout_height="wrap_content"
                android:text="@string/btn_next"/>
        <Button
                android:id="@+id/btn_stop"
                android:layout_width="70dp"
                android:layout_height="wrap_content"
                android:text="@string/btn_stop"/>
    </LinearLayout>
</LinearLayout>
```



MainActivity.java

```java

public class MainActivity extends AppCompatActivity implements Runnable {
    private static final String TAG = "MainActivity";
    int flag = 1;//设置一个标志，供点击“开始/暂停”按钮使用
    private Button btnStart, btnStop, btnNext, btnLast;
    private TextView txtInfo;
    private ListView listView;
    private SeekBar seekBar;
    private MusicService musicService;
    private Handler handler;// 处理改变进度条事件
    int UPDATE = 0x101;
    private boolean autoChange, manulChange;// 判断是进度条是自动改变还是手动改变
    private boolean isPause;// 判断是从暂停中恢复还是重新播

    AudioUtils audioUtils = new AudioUtils();
//    ArrayList<Song> songs;

    Bitmap musicFm;//音乐的封面的bitmap
    private ImageView imageView;//封面的imageView
    RotateAnimation rotateAnimation;//特效
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.d(TAG,"onCreate");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Log.d(TAG,"checkSelfPermission");
        //关于验证的函数，如果缺少这两个函数，那么需要自己开启应用的权限
        //判断权限,申请权限
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE
        ) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest
                    .permission.WRITE_EXTERNAL_STORAGE}, 1);
        } else {
            initMediaPlayer();
        }

        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.READ_EXTERNAL_STORAGE
        ) != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest
                    .permission.READ_EXTERNAL_STORAGE}, 2);
        } else {
            initMediaPlayer();
        }

    }


	//关于验证的函数
    //请求权限处理回调
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        Log.d(TAG,"onRequestPermissionsResult");
        switch (requestCode) {
            case 1:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    initMediaPlayer();
                } else {
                    Toast.makeText(this, "获取授权失败", Toast.LENGTH_SHORT).show();
                }
                break;
            case 2:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    initMediaPlayer();
                } else {
                    Toast.makeText(this, "正在获取授权", Toast.LENGTH_SHORT).show();
                }
                break;
            default:
                Toast.makeText(this, "获取授权失败", Toast.LENGTH_SHORT).show();
        }
    }


//如果有权限就会运行这里的函数
    private void initMediaPlayer() {
        
        Log.d(TAG,"init MediaPlayer ");
        //必须在获取权限后new MusicService，
        musicService = new MusicService();

        /* 非扫描的方式获取的音乐，是从数据库中直接获取
        songs =  audioUtils.getAllSongs(this);
//        for (Song song:songs){
//            musicService.test(songs.get(0));
        Bitmap fm = songs.get(0).getThumbnail();
        imageView.setImageBitmap(fm);

        Toast.makeText(this, songs.get(0).getFileName()+" "+songs.size(), Toast.LENGTH_SHORT).show();
//        }
*/

        try {
            setListViewAdapter();
        } catch (Exception e) {
            Log.i("TAG", "读取信息失败");
        }


        imageView = (ImageView) findViewById(R.id.imageView);
        btnStart = (Button) findViewById(R.id.btn_star);

        //初始化特效
        rotateAnimation = new RotateAnimation(0,360,
                Animation.RELATIVE_TO_SELF,0.5f,
                Animation.RELATIVE_TO_SELF,0.5f);
        
        //开始的监听按钮，我们可以直接从这开始
        btnStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    /**
                     * flag为1 的时候，此时player内没有东西，所以执行musicService.play()函数
                     * 进行第一次播放，然后flag自增二不再进行第一次播放
                     * 当再次点击“开始/暂停”按钮次数即大于1 将执行暂停或继续播放goplay()函数
                     */
                    if (flag == 1) {
                        btnStart.setText(R.string.btn_pause);
                        Rotate();//旋转开始
                        musicService.play();
                        flag++;
                    } else {
                        if (!musicService.player.isPlaying()) {
                            btnStart.setText(R.string.btn_pause);
                            Rotate();//旋转开始
                            musicService.goPlay();
                        } else if (musicService.player.isPlaying()) {
                            btnStart.setText(R.string.btn_star);
                            rotateAnimation.cancel();//暂停图片
                            musicService.pause();
                        }
                    }
                } catch (Exception e) {
                    Log.i("LAT", "开始异常！");
                }

            }
        });

        btnStop = (Button) findViewById(R.id.btn_stop);
        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {

                    btnStart.setText(R.string.btn_star);
                    rotateAnimation.cancel();//暂停旋转
                    musicService.stop();
                    flag = 1;//当点击停止按钮时，flag置为1
                    seekBar.setProgress(0);
                    txtInfo.setText("播放已经停止");
                } catch (Exception e) {
                    Log.i("LAT", "停止异常！");
                }

            }
        });

        btnLast = (Button) findViewById(R.id.btn_last);
        btnLast.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    btnStart.setText(R.string.btn_pause);
                    Rotate();//继续旋转
                    musicService.last();
                } catch (Exception e) {
                    Log.i("LAT", "上一曲异常！");
                }

            }
        });


        btnNext = (Button) findViewById(R.id.btn_next);
        btnNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    btnStart.setText(R.string.btn_pause);
//                    Rotate();//继续旋转
                    rotateAnimation.startNow();
                    musicService.next();
                } catch (Exception e) {
                    Log.i("LAT", "下一曲异常！");
                }

            }
        });


        seekBar = (SeekBar)

                findViewById(R.id.sb);
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {//用于监听SeekBar进度值的改变

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {//用于监听SeekBar开始拖动

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {//用于监听SeekBar停止拖动  SeekBar停止拖动后的事件
                int progress = seekBar.getProgress();
                Log.i("TAG:", "" + progress + "");
                int musicMax = musicService.player.getDuration(); //得到该首歌曲最长秒数
                int seekBarMax = seekBar.getMax();
                musicService.player
                        .seekTo(musicMax * progress / seekBarMax);//跳到该曲该秒
                autoChange = true;
                manulChange = false;
            }
        });

        txtInfo = (TextView) findViewById(R.id.tv1);

        Thread t = new Thread(this);// 自动改变进度条的线程
        //实例化一个handler对象
        handler = new

                Handler() {
                    @Override
                    public void handleMessage(Message msg) {
                        super.handleMessage(msg);
                        //更新UI
                        int mMax = musicService.player.getDuration();//最大秒数
                        if (msg.what == UPDATE) {
                            try {
                                seekBar.setProgress(msg.arg1);
                                txtInfo.setText(setPlayInfo(msg.arg2 / 1000, mMax / 1000));
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        } else {
                            seekBar.setProgress(0);
                            txtInfo.setText("播放已经停止");
                        }
                    }
                }

        ;
        t.start();

    }
    
    //向列表添加MP3名字，和listView有关的函数
    private void setListViewAdapter() {
        Log.d(TAG,"musicList.size:"+musicService.musicList.size());
        String[] str = new String[musicService.musicList.size()];
        int i = 0;
        for (String path : musicService.musicList) {
            File file = new File(path);
            str[i++] = file.getName();
        }
        ArrayAdapter adapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1,str);
        listView = (ListView) findViewById(R.id.lv1);
        listView.setAdapter(adapter);

        //通过播放的音乐路径来得到音乐大的封面
        String dataSource = musicService.musicList.get(musicService.songNum);//得到当前播放音乐的路径
        musicFm =  audioUtils.createAlbumArt(dataSource);
        imageView.setImageBitmap(musicFm);
    }

    @Override
    public void run() {//这里需要新开一个线程在后台播放，同时需要控制bar，因此需要service通信
        int position, mMax, sMax;
        while (!Thread.currentThread().isInterrupted()) {
            if (musicService.player != null && musicService.player.isPlaying()) {
                position = musicService.getCurrentProgress();//得到当前歌曲播放进度(秒)
                mMax = musicService.player.getDuration();//最大秒数
                sMax = seekBar.getMax();//seekBar最大值，算百分比
                Message m = handler.obtainMessage();//获取一个Message
                m.arg1 = position * sMax / mMax;//seekBar进度条的百分比
                m.arg2 = position;
                m.what = UPDATE;
                handler.sendMessage(m);
                //  handler.sendEmptyMessage(UPDATE);
                try {
                    Thread.sleep(1000);// 每间隔1秒发送一次更新消息
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

        }

    }


    //设置当前播放的信息
    private String setPlayInfo(int position, int max) {
        //设置图片
        String dataSource = musicService.musicList.get(musicService.songNum);//得到当前播放音乐的路径
        musicFm =  audioUtils.createAlbumArt(dataSource);
        imageView.setImageBitmap(musicFm);
        //设置音乐信息
        String info = "正在播放:  " + musicService.songName + "\t\t";
        int pMinutes = 0;
        while (position >= 60) {
            pMinutes++;
            position -= 60;
        }
        String now = (pMinutes < 10 ? "0" + pMinutes : pMinutes) + ":"
                + (position < 10 ? "0" + position : position);

        int mMinutes = 0;
        while (max >= 60) {
            mMinutes++;
            max -= 60;
        }
        String all = (mMinutes < 10 ? "0" + mMinutes : mMinutes) + ":"
                + (max < 10 ? "0" + max : max);

        return info + now + " / " + all;
    }

    //音乐封面旋转特效
    public void Rotate(){
//        AnimationSet animationSet = new AnimationSet(true);

        rotateAnimation.setDuration(20000);//设定转一圈的时间
        rotateAnimation.setRepeatCount(Animation.INFINITE);//设定无限循环
        rotateAnimation.setRepeatMode(Animation.RESTART);//

//        animationSet.addAnimation(rotateAnimation);
        imageView.startAnimation(rotateAnimation);
    }

}
```



我的MusicService文件

```java

public class MusicService {
    private static final File PATH = Environment.getExternalStorageDirectory();// 获取SD卡总目录。
    public List<String> musicList;// 存放找到的所有mp3的绝对路径。
    public MediaPlayer player; // 定义多媒体对象
    public int songNum; // 当前播放的歌曲在List中的下标,flag为标致
    public String songName; // 当前播放的歌曲名

    class MusicFilter implements FilenameFilter {
        public boolean accept(File dir, String name) {
            return (name.endsWith(".mp3"));//返回当前目录所有以.mp3结尾的文件
        }
    }

    public MusicService() {
        super();
        player = new MediaPlayer();
        musicList = new ArrayList<String>();
        try {
            File MUSIC_PATH = new File(PATH, "netease/cloudmusic/Music");//获取Music文件的二级目录
            if (MUSIC_PATH.listFiles(new MusicFilter()).length > 0) {
                for (File file : MUSIC_PATH.listFiles(new MusicFilter())) {

                    musicList.add(file.getAbsolutePath());
                }
            }
        } catch (Exception e) {
            Log.i("TAG", "读取文件异常");
        }

    }

    public void setPlayName(String dataSource) {
        File file = new File(dataSource);//假设为D:\\mm.mp3
        String name = file.getName();//name=mm.mp3
        int index = name.lastIndexOf(".");//找到最后一个.
        songName = name.substring(0, index);//截取为mm
    }

    public void play() {
        try {
            player.reset(); //重置多媒体
            String dataSource = musicList.get(songNum);//得到当前播放音乐的路径
            setPlayName(dataSource);//截取歌名
            // 指定参数为音频文件
            player.setAudioStreamType(AudioManager.STREAM_MUSIC);
            player.setDataSource(dataSource);//为多媒体对象设置播放路径
            player.prepare();//准备播放
            player.start();//开始播放
            //setOnCompletionListener 当当前多媒体对象播放完成时发生的事件
            player.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                public void onCompletion(MediaPlayer arg0) {
                    next();//如果当前歌曲播放完毕,自动播放下一首.
                }
            });

        } catch (Exception e) {
            Log.v("MusicService", e.getMessage());
        }
    }
    /*和数据库有关的
    public void test(Song song){//测试数据库
        try {
            player.reset(); //重置多媒体

            String dataSource = song.getFileUrl();
//            String dataSource = musicList.get(songNum);//得到当前播放音乐的路径
            setPlayName(dataSource);//截取歌名
            // 指定参数为音频文件
            player.setAudioStreamType(AudioManager.STREAM_MUSIC);
            player.setDataSource(dataSource);//为多媒体对象设置播放路径
            player.prepare();//准备播放
            player.start();//开始播放
            //setOnCompletionListener 当当前多媒体对象播放完成时发生的事件
            player.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                public void onCompletion(MediaPlayer arg0) {
                    next();//如果当前歌曲播放完毕,自动播放下一首.
                }
            });

        } catch (Exception e) {
            Log.v("MusicService", e.getMessage());
        }
    }
*/
    //继续播放
    public void goPlay() {
        int position = getCurrentProgress();
        player.seekTo(position);//设置当前MediaPlayer的播放位置，单位是毫秒。
        try {
            player.prepare();//  同步的方式装载流媒体文件。
        } catch (Exception e) {
            e.printStackTrace();
        }
        player.start();
    }

    // 获取当前进度
    public int getCurrentProgress() {
        if (player != null & player.isPlaying()) {
            return player.getCurrentPosition();
        } else if (player != null & (!player.isPlaying())) {
            return player.getCurrentPosition();
        }
        return 0;
    }

    public void next() {
        songNum = songNum == musicList.size() - 1 ? 0 : songNum + 1;
        play();
    }

    public void last() {
        songNum = songNum == 0 ? musicList.size() - 1 : songNum - 1;
        play();
    }

    // 暂停播放
    public void pause() {
        if (player != null && player.isPlaying()) {
            player.pause();
        }
    }

    public void stop() {
        if (player != null && player.isPlaying()) {
            player.stop();
            player.reset();
        }
    }
}

```



我的圆形封面

```java
package cn.study.euraxluo.androidtup;/* AndroidTup
 * cn.study.euraxluo.androidtup
 * CircleImageView
 * 2019/5/13 13:26
 * author:Euraxluo
 * TODO
 */

import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.widget.ImageView;

public class CircleImageView extends android.support.v7.widget.AppCompatImageView {
    private Paint mPaintBitmap = new Paint(Paint.ANTI_ALIAS_FLAG);
    private Bitmap mRawBitmap;
    private BitmapShader mShader;
    private Matrix mMatrix = new Matrix();

    public CircleImageView(Context context,AttributeSet attrs) {
        super(context, attrs);
    }

    @Override

    protected void onDraw(Canvas canvas) {
        Bitmap rawBitmap = getBimap(getDrawable());
        if (rawBitmap != null) {
            int viewWidth = getWidth();
            int viewHeight = getHeight();
            int viewMinSize = Math.min(viewWidth, viewHeight);
            float dstHeight = viewMinSize;
            float dstWidth = viewMinSize;
            if (mShader == null || !rawBitmap.equals(mRawBitmap)) {
                mRawBitmap = rawBitmap;
                mShader = new BitmapShader(mRawBitmap, Shader.TileMode.CLAMP, Shader.TileMode.CLAMP);
            }
            if (mShader != null) {
                mMatrix.setScale(dstWidth / rawBitmap.getWidth(), dstHeight / rawBitmap.getHeight());
                mShader.setLocalMatrix(mMatrix);
            }
            mPaintBitmap.setShader(mShader);
            float radius = viewMinSize / 2.0f;
            canvas.drawCircle(radius, radius, radius, mPaintBitmap);
        } else super.onDraw(canvas);
    }

    private Bitmap getBimap(Drawable drawable) {
        if (drawable instanceof BitmapDrawable) {
            return ((BitmapDrawable) drawable).getBitmap();
        } else if (drawable instanceof ColorDrawable) {
            Rect rect = drawable.getBounds();
            int width = rect.right - rect.left;
            int height = rect.bottom - rect.top;
            int color = ((ColorDrawable) drawable).getColor();
            Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(bitmap);
            canvas.drawARGB(Color.alpha(color), Color.red(color), Color.green(color), Color.blue(color));
            return bitmap;
        } else return null;
    }

}

```



---

数据库扫描用的：Song实体类

```java
package cn.study.euraxluo.androidtup;

import android.graphics.Bitmap;

public class Song {


    private String fileName;
    private String title;
    private int duration;
    private String singer;
    private String album;
    private String year;
    private String type;
    private String size;
    private String fileUrl;
    private Bitmap Thumbnail;

    public Bitmap getThumbnail() {
        return Thumbnail;
    }

    public void setThumbnail(Bitmap thumbnail) {
        Thumbnail = thumbnail;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getDuration() {
        return duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public String getSinger() {
        return singer;
    }

    public void setSinger(String singer) {
        this.singer = singer;
    }

    public String getAlbum() {
        return album;
    }

    public void setAlbum(String album) {
        this.album = album;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getSize() {
        return size;
    }

    public void setSize(String size) {
        this.size = size;
    }

    public String getFileUrl() {
        return fileUrl;
    }

    public void setFileUrl(String fileUrl) {
        this.fileUrl = fileUrl;
    }

    public Song() {
        super();
    }

    public Song(String fileName, String title, int duration, String singer,
                String album, String year, String type, String size, String fileUrl) {
        super();
        this.fileName = fileName;
        this.title = title;
        this.duration = duration;
        this.singer = singer;
        this.album = album;
        this.year = year;
        this.type = type;
        this.size = size;
        this.fileUrl = fileUrl;
    }

    @Override
    public String toString() {
        return "Song [fileName=" + fileName + ", title=" + title
                + ", duration=" + duration + ", singer=" + singer + ", album="
                + album + ", year=" + year + ", type=" + type + ", size="
                + size + ", fileUrl=" + fileUrl + "]";
    }

}
```

扫描数据的AudioUtils.java

```java
package cn.study.euraxluo.androidtup;


import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.MediaMetadataRetriever;
import android.provider.MediaStore;

import java.util.ArrayList;

public class AudioUtils {

    /**
     * 获取sd卡所有的音乐文件
     *
     * @return
     * @throws Exception
     */
    public static ArrayList<Song> getAllSongs(Context context) {

        ArrayList<Song> songs = null;

        Cursor cursor = context.getContentResolver().query(
                MediaStore.Audio.Media.EXTERNAL_CONTENT_URI,
                new String[] { MediaStore.Audio.Media._ID,
                        MediaStore.Audio.Media.DISPLAY_NAME,
                        MediaStore.Audio.Media.TITLE,
                        MediaStore.Audio.Media.DURATION,
                        MediaStore.Audio.Media.ARTIST,
                        MediaStore.Audio.Media.ALBUM,
                        MediaStore.Audio.Media.YEAR,
                        MediaStore.Audio.Media.MIME_TYPE,
                        MediaStore.Audio.Media.SIZE,
                        MediaStore.Audio.Media.DATA },
                MediaStore.Audio.Media.MIME_TYPE + "=? or "
                        + MediaStore.Audio.Media.MIME_TYPE + "=?",
                new String[] { "audio/mpeg", "audio/x-ms-wma" }, null);

        songs = new ArrayList<Song>();

        if (cursor.moveToFirst()) {

            Song song = null;

            do {
                song = new Song();
                // 文件名
                song.setFileName(cursor.getString(1));
                // 歌曲名
                song.setTitle(cursor.getString(2));
                // 时长
                song.setDuration(cursor.getInt(3));
                // 歌手名
                song.setSinger(cursor.getString(4));
                // 专辑名
                song.setAlbum(cursor.getString(5));
                // 年代
                if (cursor.getString(6) != null) {
                    song.setYear(cursor.getString(6));
                } else {
                    song.setYear("未知");
                }
                // 歌曲格式
                if ("audio/mpeg".equals(cursor.getString(7).trim())) {
                    song.setType("mp3");
                } else if ("audio/x-ms-wma".equals(cursor.getString(7).trim())) {
                    song.setType("wma");
                }
                // 文件大小
                if (cursor.getString(8) != null) {
                    float size = cursor.getInt(8) / 1024f / 1024f;
                    song.setSize((size + "").substring(0, 4) + "M");
                } else {
                    song.setSize("未知");
                }
                // 文件路径
                if (cursor.getString(9) != null) {
                    song.setFileUrl(cursor.getString(9));
                }

                //获取专辑封面（如果数据量大的话，会很耗时——需要考虑如何开辟子线程加载）
                Bitmap albumArt = createAlbumArt(song.getFileUrl());
                song.setThumbnail(albumArt);
                
                songs.add(song);
            } while (cursor.moveToNext());

            cursor.close();

        }
        return songs;
    }

    public static int calculateInSampleSize(BitmapFactory.Options options,int reqWidth,int reqHeight){
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;
        if(height > reqHeight || width > reqWidth){
            final int halfHeight = height/2;
            final int halfWidth = width/2;
            while ((halfHeight/inSampleSize)>reqHeight && (halfWidth/inSampleSize)>reqWidth) inSampleSize*=2;
        }
        return inSampleSize;
    }
    public static Bitmap createAlbumArt(final String filePath) {
        Bitmap bitmap = null;
        //能够获取多媒体文件元数据的类
        MediaMetadataRetriever retriever = new MediaMetadataRetriever();
        try {
            retriever.setDataSource(filePath); //设置数据源

            byte[] embedPic = retriever.getEmbeddedPicture(); //得到字节型数据
            final BitmapFactory.Options options = new BitmapFactory.Options();
            options.inJustDecodeBounds = true;
            BitmapFactory.decodeByteArray(embedPic, 0, embedPic.length,options);
            options.inSampleSize = calculateInSampleSize(options,100,100);
            options.inJustDecodeBounds = false;
            bitmap = BitmapFactory.decodeByteArray(embedPic, 0, embedPic.length,options); //转换为图片
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                retriever.release();
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
        return bitmap;
    }
}
```

