// 藏品详情页面逻辑
import { api } from '../../utils/api.js';
import config from '../../config/index.js';
import audioManager from '../../utils/audioManager.js'; // 导入全局音频管理器

Page({
  /**
   * 页面的初始数据
   */
  data: {
    scrollTop: 0,
    showTitle: false,
    isFavorite: false,
    isLoading: true,
    static_url: config.STATIC_URL, //静态资源地址
    collection: {
      id: '',
      name: '',
      description: '',
      type: '',
      size: '',
      material: '',
      age: '',
      author: '',
      collector: '',
      mediaList: [] // 包含图片、音频等多媒体信息
    },
    showFullIntro: false,
    introText: '',
    // 音频相关数据
    currentAudioUrl: '',
    currentAudioName: '',
    audioState: 'stopped', // 'playing', 'paused', 'stopped'
    hasAudio: false,
    hasImage: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取传递的藏品ID参数
    // console.log(options.collection);
    const collection = JSON.parse(options.collection);
    const collectionId = collection.id;
    
    if (!collectionId) {
      console.error('缺少藏品ID参数');
      wx.showToast({
        title: '参数错误',
        icon: 'error'
      });
      return;
    }

    // 加载藏品详情数据
    this.loadCollectionDetail(collectionId);
    
    // 初始化音频管理器回调
    this.initAudioCallbacks();
  },
  
  /**
   * 初始化音频管理器回调
   */
  initAudioCallbacks: function() {
    // 注册音频播放事件回调
    audioManager.on('onPlay', () => {
      this.setData({
        audioState: 'playing',
        currentAudioUrl: audioManager.getCurrentAudioUrl(),
        currentAudioName: audioManager.getCurrentAudioName()
      });
    });
    
    // 注册音频暂停事件回调
    audioManager.on('onPause', () => {
      this.setData({
        audioState: 'paused'
      });
    });
    
    // 注册音频停止事件回调
    audioManager.on('onStop', () => {
      this.setData({
        audioState: 'stopped',
        currentAudioUrl: '',
        currentAudioName: ''
      });
    });
    
    // 注册音频播放结束事件回调
    audioManager.on('onEnded', () => {
      this.setData({
        audioState: 'stopped',
        currentAudioUrl: '',
        currentAudioName: ''
      });
      wx.showToast({
        title: '音频播放完毕',
        icon: 'none'
      });
    });
    
    // 注册音频播放错误事件回调
    audioManager.on('onError', (res) => {
      this.setData({
        audioState: 'stopped',
        currentAudioUrl: '',
        currentAudioName: ''
      });
      wx.showToast({
        title: '音频播放失败',
        icon: 'error'
      });
    });
  },

  /**
   * 更新藏品介绍显示
   */
  updateIntroDisplay: function(description) {
    const maxLength = 100;
    let introText = '';
    
    if (description && description.length > maxLength) {
      introText = this.data.showFullIntro ? description : description.substring(0, maxLength) + '...';
    } else {
      introText = description || '暂无详细介绍';
    }
    
    this.setData({
      introText: introText
    });
  },

  /**
   * 加载藏品详情数据
   */
  /**
   * 加载藏品详情数据
   */
  loadCollectionDetail: async function(collectionId) {
    wx.showLoading({
      title: '加载中...'
    });
  
    try {
      // 调用后端API获取藏品详情
      const res = await api.getCollectionDetail(collectionId);
      
      if (res.code === 200) {
        const collection = res.data;
        
        // 处理媒体列表
        let mediaList = collection.mediaList || [];
        
        // 更新页面数据
        this.setData({
          collection: collection,
          mediaList: mediaList,
          hasAudio: collection.hasAudio || false,
          hasImage: collection.hasImage || false,
          audioUrl: collection.audioUrl || '',
          currentIndex: 0,
          isLoading: false
        });
        
            // 更新藏品介绍显示
        this.updateIntroDisplay(collection.description);
        // console.log('藏品详情加载成功:', collection);
        // console.log(mediaList)
      } else {
        throw new Error(res.msg || '获取藏品详情失败');
      }
    } catch (error) {
      console.error('加载藏品详情失败:', error);
      wx.showToast({
        title: error.message || '加载失败',
        icon: 'none'
      });
      
      // 设置错误状态
      this.setData({
        loading: false,
        error: true
      });
    } finally {
      wx.hideLoading();
    }
  },

  /**
   * 点击图片全屏预览
   */
  previewImage: function(e) {
    const index = e.currentTarget.dataset.index;
    const media_src = this.data.collection.mediaList
      .filter(item=>item.type===1 || item.type===2)
      .map(image=>({
        url: this.data.static_url + image.url,
        type: image.type===1?'image':'video',
        poster: this.data.static_url + image.url
      }));
    console.log(media_src)
    wx.previewMedia({
      sources: media_src,
      current: index,
      showmenu: true
    });
  },

  /**
   * 播放藏品音频
   */
  playCollectionAudio: function () {
    // 查找音频媒体
    const audioMedia = this.data.collection.mediaList.find(media => media.type === 2);
    
    if (!audioMedia || !audioMedia.url) {
      wx.showToast({
        title: '暂无音频',
        icon: 'none'
      });
      return;
    }
    
    // 使用全局音频管理器播放音频
    audioManager.play(
      this.data.static_url + audioMedia.url, 
      this.data.collection.name || '藏品语音讲解',
      '藏品详情',
      this.data.collection.author || '未知作者',
      this.data.static_url + (this.data.collection.mediaList.find(media => media.type === 0)?.url || '/wx_static/tmp_images/placeholder_image.png')
    );
  },

  /**
   * 切换藏品介绍显示状态
   */
  toggleIntro: function () {
    this.setData({
      showFullIntro: !this.data.showFullIntro
    });
    
    // 更新藏品介绍显示
    this.updateIntroDisplay(this.data.collection.description);
  },

  /**
   * 页面滚动事件处理
   */
  onScroll: function (e) {
    const scrollTop = e.detail.scrollTop;
    // 当滚动超过一定距离时显示标题
    if (scrollTop > 200 && !this.data.showTitle) {
      this.setData({
        showTitle: true
      });
    } else if (scrollTop <= 200 && this.data.showTitle) {
      this.setData({
        showTitle: false
      });
    }
  },

  /**
   * 返回上一页
   */
  goBack: function () {
    wx.navigateBack({
      delta: 1
    });
  },

  /**
   * 收藏藏品
   */
  collectCollection: function () {
    this.setData({
      isFavorite: !this.data.isFavorite
    });

    if (this.data.isFavorite) {
      wx.showToast({
        title: '已收藏',
        icon: 'success'
      });
    } else {
      wx.showToast({
        title: '已取消收藏',
        icon: 'none'
      });
    }
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    return {
      title: this.data.collection.name || '藏品详情',
      path: `/pages/collection_detail/index?id=${this.data.collection.id}`
    };
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    // 重新加载当前藏品详情
    const collectionId = this.data.collection.id;
    if (collectionId) {
      this.loadCollectionDetail(collectionId);
      wx.stopPullDownRefresh();
    }
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    // 页面显示时更新音频状态
    this.setData({
      audioState: audioManager.getState(),
      currentAudioUrl: audioManager.getCurrentAudioUrl(),
      currentAudioName: audioManager.getCurrentAudioName()
    });
  }
});