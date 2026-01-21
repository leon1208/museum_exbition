// 展览单元详情页面逻辑
import { api } from '../../utils/api.js';
import config from '../../config/index.js';

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
      hasAudio: false
    },
    currentIndex: 0, // 当前轮播图索引
    showFullIntro: false,
    introText: '',
    // 音频相关数据
    audioContext: null,
    isAudioPlaying: false,
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
            if (media.type === 1) { // 图片类型
              images.push(media.url);
            } else if (media.type === 2) { // 音频类型
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
            unitType: unitData.unitType || unitData.unit_type || 0,
            section: unitData.section || '',
            images: images,
            audioUrl: audioUrl,
            hasAudio: hasAudio
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
    const urls = this.data.unit.images;
    
    wx.previewImage({
      current: urls[index],
      urls: urls
    });
  },

  /**
   * 播放音频
   */
  playAudio: function () {
    const audioUrl = this.data.unit.audioUrl;
    const audioName = this.data.unit.name || '展览单元音频';
    
    if (!audioUrl) {
      wx.showToast({
        title: '暂无音频',
        icon: 'none'
      });
      return;
    }
    
    // 如果当前正在播放同一个音频，则切换暂停/继续
    if (this.data.currentAudioUrl === audioUrl && this.data.audioContext) {
      if (this.data.audioState === 'playing') {
        // 暂停当前音频
        this.data.audioContext.pause();
        this.setData({
          audioState: 'paused'
        });
        wx.showToast({
          title: '已暂停',
          icon: 'none'
        });
      } else if (this.data.audioState === 'paused') {
        // 继续播放当前音频
        this.data.audioContext.play();
        this.setData({
          audioState: 'playing'
        });
        wx.showToast({
          title: '继续播放',
          icon: 'none'
        });
      }
      return;
    }
    
    // 如果有其他音频正在播放，停止它
    if (this.data.audioContext && this.data.audioState === 'playing') {
      this.data.audioContext.stop();
    }
    
    // 创建内部 audio 上下文 InnerAudioContext 对象
    const innerAudioContext = wx.createInnerAudioContext();

    // 关键配置：设置是否遵循系统静音开关，iOS静音模式下仍可播放
    innerAudioContext.autoplay = false;
    innerAudioContext.loop = false;
    innerAudioContext.obeyMuteSwitch = false;
    innerAudioContext.audioCategory = 'playback';
    
    // 设置音频文件的路径
    innerAudioContext.src = this.data.static_url + audioUrl;
    
    // 监听音频播放事件
    innerAudioContext.onPlay(() => {
      this.setData({
        audioState: 'playing',
        currentAudioUrl: audioUrl,
        currentAudioName: audioName,
        audioContext: innerAudioContext
      });
      wx.showToast({
        title: '音频播放中...',
        icon: 'none'
      });
    });
    
    // 监听音频暂停事件
    innerAudioContext.onPause(() => {
      this.setData({
        audioState: 'paused'
      });
    });
    
    // 监听音频停止事件
    innerAudioContext.onStop(() => {
      this.setData({
        audioState: 'stopped',
        currentAudioUrl: '',
        currentAudioName: ''
      });
    });
    
    // 监听音频播放结束事件
    innerAudioContext.onEnded(() => {
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
    
    // 监听音频播放错误事件
    innerAudioContext.onError((res) => {
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
    
    // 播放音频
    innerAudioContext.play();
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
    // 销毁音频上下文，释放资源
    if (this.data.audioContext) {
      this.data.audioContext.destroy();
    }
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