import os, platform

# 设置VLC库路径，需在import vlc之前
os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.12/"

import vlc

class Player:

    def __init__(self, *args):
        if args:
            self.instance = vlc.Instance(*args)
        else:
            self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.uri = None

    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.uri = uri
        # self.mediaplayer.set_mrl(self.uri)    
        # 替换为 set_media 方法，以获取进度
        m = self.instance.media_new(uri)
        self.mediaplayer.set_media(m)

    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.mediaplayer.play()
        else:
            return self.mediaplayer.play()

    # 暂停
    def pause(self):
        self.mediaplayer.pause()

    # 恢复
    def resume(self):
        self.mediaplayer.set_pause(0)

    # 停止
    def stop(self):
        self.mediaplayer.stop()

    # 释放资源
    def release(self):
        return self.mediaplayer.release()

    # 是否正在播放
    def is_playing(self):
        return self.mediaplayer.is_playing()

    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.mediaplayer.get_time()

    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.mediaplayer.get_time()

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.mediaplayer.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.mediaplayer.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.mediaplayer.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.mediaplayer.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.mediaplayer.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.mediaplayer.set_position(float_val)

    # 获取当前文件播放速率
    def get_rate(self):
        return self.mediaplayer.get_rate()

    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.mediaplayer.set_rate(rate)

    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.mediaplayer.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.mediaplayer.video_set_aspect_ratio(ratio)

    # 设置窗口句柄
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.mediaplayer.set_hwnd(wm_id)
        elif platform.system() == 'Linux':
            self.mediaplayer.set_xwindow(wm_id)
        else:  # MacOS
            self.mediaplayer.set_nsobject(wm_id)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.mediaplayer.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.mediaplayer.event_manager().event_detach(event_type, callback)
