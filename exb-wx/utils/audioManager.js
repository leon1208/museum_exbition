// 全局音频播放管理器
class AudioManager {
  constructor() {
    // 获取全局唯一的背景音频管理器
    this.backgroundAudioManager = wx.getBackgroundAudioManager();
    this.currentAudioUrl = '';
    this.currentAudioName = '';
    this.currentAudioState = 'stopped'; // 'playing', 'paused', 'stopped'
    this.callbacks = {};
    
    // 初始化事件监听
    this.initEventListeners();
  }
  
  // 初始化事件监听
  initEventListeners() {
    // 监听播放事件
    this.backgroundAudioManager.onPlay(() => {
      this.currentAudioState = 'playing';
      this.triggerCallback('onPlay');
    });
    
    // 监听暂停事件
    this.backgroundAudioManager.onPause(() => {
      this.currentAudioState = 'paused';
      this.triggerCallback('onPause');
    });
    
    // 监听停止事件
    this.backgroundAudioManager.onStop(() => {
      this.currentAudioState = 'stopped';
      this.currentAudioUrl = '';
      this.currentAudioName = '';
      this.triggerCallback('onStop');
    });
    
    // 监听播放结束事件
    this.backgroundAudioManager.onEnded(() => {
      this.currentAudioState = 'stopped';
      this.currentAudioUrl = '';
      this.currentAudioName = '';
      this.triggerCallback('onEnded');
    });
    
    // 监听错误事件
    this.backgroundAudioManager.onError((res) => {
      this.currentAudioState = 'stopped';
      this.triggerCallback('onError', res);
    });
  }
  
  // 注册回调函数
  on(event, callback) {
    if (typeof callback === 'function') {
      this.callbacks[event] = callback;
    }
  }
  
  // 触发回调函数
  triggerCallback(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event](data);
    }
  }
  
  // 播放音频
  play(audioUrl, audioName = '未知音频', albumName = '', artistName = '', coverUrl = '') {
    if (!audioUrl) {
      wx.showToast({
        title: '暂无音频',
        icon: 'none'
      });
      return;
    }
    
    // 如果当前正在播放同一个音频，则切换暂停/继续
    if (this.currentAudioUrl === audioUrl) {
      if (this.currentAudioState === 'playing') {
        this.pause();
        return;
      } else if (this.currentAudioState === 'paused') {
        this.resume();
        return;
      }
    }
    
    // 设置音频信息
    this.backgroundAudioManager.title = audioName;
    this.backgroundAudioManager.src = audioUrl;
    
    // 设置专辑名、作者和封面图
    if (albumName) {
      this.backgroundAudioManager.epname = albumName;
    }
    if (artistName) {
      this.backgroundAudioManager.singer = artistName;
    }
    if (coverUrl) {
      this.backgroundAudioManager.coverImgUrl = coverUrl;
    }
    
    // 记录当前播放的音频
    this.currentAudioUrl = audioUrl;
    this.currentAudioName = audioName;
  }
  
  // 暂停音频
  pause() {
    this.backgroundAudioManager.pause();
  }
  
  // 继续播放音频
  resume() {
    this.backgroundAudioManager.play();
  }
  
  // 停止音频
  stop() {
    this.backgroundAudioManager.stop();
  }
  
  // 获取当前音频状态
  getState() {
    return this.currentAudioState;
  }
  
  // 获取当前播放的音频URL
  getCurrentAudioUrl() {
    return this.currentAudioUrl;
  }
  
  // 获取当前播放的音频名称
  getCurrentAudioName() {
    return this.currentAudioName;
  }
}

// 导出单例实例
const audioManager = new AudioManager();
export default audioManager;