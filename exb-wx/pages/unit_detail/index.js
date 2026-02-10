// 展览单元详情页面逻辑
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
    unit: {
      id: '',
      name: '',
      description: '',
      guideText: '',
      exhibitLabel: '',
      unitType: 0, // 0展品单元 1文字单元 2多媒体单元
      section: '',
      images: [],
      audioUrl: '',
      hasAudio: false,
      videoUrl: '',
      hasVideo: false,
      collectionsDetail: [] // 新增：关联的藏品详情
    },
    currentIndex: 0, // 当前轮播图索引
    showFullIntro: false,
    introText: '',
    // 音频相关数据
    currentAudioUrl: '',
    currentAudioName: '',
    audioState: 'stopped' // 'playing', 'paused', 'stopped'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取传递的展览单元ID参数
    const unitId = options.id;
    const unitName = decodeURIComponent(options.name || '');
    const description = decodeURIComponent(options.description || '');
    
    if (!unitId) {
      console.error('缺少展览单元ID参数');
      wx.showToast({
        title: '参数错误',
        icon: 'error'
      });
      return;
    }

    // 先使用传入的参数初始化页面
    this.setData({
      unit: {
        id: unitId,
        name: unitName,
        description: description
      }
    });

    // 加载展览单元详情数据
    this.loadUnitDetail(unitId);
    
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
   * 更新导览词显示
   */
  updateIntroDisplay: function(guideText) {
    const maxLength = 100;
    let introText = '';
    
    if (guideText && guideText.length > maxLength) {
      introText = this.data.showFullIntro ? guideText : guideText.substring(0, maxLength) + '...';
    } else {
      introText = guideText || '暂无导览词';
    }
    
    this.setData({
      introText: introText
    });
  },

  /**
   * 加载展览单元详情数据
   */
  loadUnitDetail: async function(unitId) {
    try {
      // 注意：这里需要后端提供获取单个展览单元详情的API
      // 暂时使用模拟数据，实际开发时需要调用真实的API
      const response = await api.getUnitDetail(unitId);
      
      if (response.code === 200) {
        const unitData = response.data;
        
        // 提取媒体信息
        const images = [];
        let audioUrl = '';
        let hasAudio = false;
        
        if (unitData.mediaList && Array.isArray(unitData.mediaList)) {
          unitData.mediaList.forEach(media => {
            if (media.type === 1 || media.type === 2) { // 图片和视频类型
              images.push(media);
            } else if (media.type === 3) { // 音频类型
              audioUrl = media.url;
              hasAudio = true;
            }
          });
        }
        
        // 更新展览单元基本信息
        this.setData({
          unit: {
            id: unitData.id || unitId,
            name: unitData.name || unitData.unit_name || this.data.unit.name,
            description: unitData.description || this.data.unit.description,
            guideText: unitData.guideText || unitData.guide_text || '',
            exhibitLabel: unitData.exhibitLabel || unitData.exhibit_label || '',
            unitType: unitData.type || 0,
            section: unitData.section || '',
            images: images,
            audioUrl: unitData.audioUrl || audioUrl,
            hasAudio: unitData.hasAudio || hasAudio,
            videoUrl: unitData.videoUrl || '',
            hasVideo: unitData.hasVideo || false,
            collectionsDetail: unitData.collectionsDetail || [] // 添加关联藏品详情
          },
          isLoading: false
        });
        
        // 更新导览词显示
        this.updateIntroDisplay(unitData.guideText || unitData.guide_text || '');
      } else {
        throw new Error(response.msg || '获取展览单元详情失败');
      }
    } catch (error) {
      console.error('加载展览单元详情失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'error'
      });
      this.setData({
        isLoading: false
      });
    }
  },

  /**
   * 图片轮播切换事件
   */
  onSwiperChange: function(e) {
    this.setData({
      currentIndex: e.detail.current
    });
  },

  /**
   * 点击图片全屏预览
   */
  previewImage: function(e) {
    const index = e.currentTarget.dataset.index;
    const images = this.data.unit.images;
    
    // 为每个图片URL添加static_url前缀
    // const fullUrls = images.map(image => this.data.static_url + image.mediaUrl);
    const media_src = images.map(image => ({
      url: this.data.static_url + image.mediaUrl,
      type: image.type===1?'image':'video',
      poster: this.data.static_url + image.url
    }));
    wx.previewMedia({
      sources: media_src,
      current: index,
      showmenu: true
    });
    
    // if (images[index].type === 2 || images[index].type === 1) { // 视频类型
    //   // 视频类型不支持全屏预览，直接播放
    //   wx.previewMedia({
    //     sources: [{
    //         url: fullUrls[index],
    //         type: images[index].type===1?'image':'video',
    //         poster: images[0] ? this.data.static_url + images[index].url : '' // 使用第一张图片作为视频封面
    //     }],
    //     current: 0,
    //     showmenu: true
    //   });
    // } else {
    //   wx.previewImage({
    //     current: fullUrls[index], // 当前预览的图片URL
    //     urls: fullUrls // 所有预览的图片URL数组
    //   });
    // }
  },

  /**
   * 播放音频
   */
  playUnitAudio: function (e) {
    const audioUrl = this.data.unit.audioUrl;
    const audioName = this.data.unit.name || '展览单元音频';
    const albumName = e.currentTarget.dataset.albumName || '';
    const artistName = e.currentTarget.dataset.artistName || '';
    const coverUrl = e.currentTarget.dataset.coverUrl || '';

    if (!audioUrl) {
      wx.showToast({
        title: '暂无音频',
        icon: 'none'
      });
      return;
    }
    
    // 使用全局音频管理器播放音频
    audioManager.play(this.data.static_url + audioUrl, audioName, albumName, artistName, coverUrl);
  },

  /**
   * 跳转到藏品详情页面
   */
  goToCollectionDetail: function(e) {
    const collection = e.currentTarget.dataset.collection;
    wx.navigateTo({
      url: '../collection_detail/index?collection=' + JSON.stringify(collection)
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

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
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    // 页面卸载时不需要销毁音频管理器，因为它是全局的
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    // 重新加载当前展览单元详情
    const unitId = this.data.unit.id;
    if (unitId) {
      this.loadUnitDetail(unitId);
      wx.stopPullDownRefresh();
    }
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
   * 切换收藏状态
   */
  toggleFavorite: function () {
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
   * 切换导览词显示状态
   */
  toggleIntro: function () {
    this.setData({
      showFullIntro: !this.data.showFullIntro
    });
    
    // 更新导览词显示
    this.updateIntroDisplay(this.data.unit.guideText || this.data.unit.description);
  }
});