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
    hasAudioMedia: false,
    hasImageMedia: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取传递的藏品ID参数
    console.log(options.collection);
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
    try {
      // 使用模拟数据替代API调用
      const mockCollectionData = {
        id: collectionId,
        name: '青花瓷瓶',
        description: '这件青花瓷瓶制作于明代永乐年间，高约45厘米，口径12厘米，底径15厘米。瓶身绘有精美的缠枝莲纹，釉色莹润，青花发色纯正。此瓶造型端庄，纹饰精美，是明代青花瓷器的典型代表作品。',
        type: '瓷器',
        size: '高45cm × 口径12cm × 底径15cm',
        material: '瓷',
        age: '明代永乐年间',
        author: '景德镇窑',
        collector: '故宫博物院',
        mediaList: [
          {
            id: 1,
            type: 0, // 0 表示图片
            url: '/museum/media/2026/01/16/4339f7e57eea40c4a4a8b8d361cded12.JPG',
            description: '正面视图'
          },
          {
            id: 2,
            type: 0, // 0 表示图片
            url: '/museum/media/2026/01/16/7b2acdaf01ab46c4b2bdee94f2932f3d.JPG',
            description: '正面视图'
          },
          {
            id: 4,
            type: 2, // 2 表示音频
            url: '/museum/media/2026/01/16/bcf5cd3d41294749a1f71f0d5715c805.wav',
            description: '语音讲解'
          }
        ]
      };
  
      // 检查是否有音频和图片媒体
      let hasAudioMedia = false;
      let hasImageMedia = false;
      
      if (mockCollectionData.mediaList && Array.isArray(mockCollectionData.mediaList)) {
        hasAudioMedia = mockCollectionData.mediaList.some(media => media.type === 2); // 假设type为2表示音频
        hasImageMedia = mockCollectionData.mediaList.some(media => media.type === 0); // 假设type为0表示图片
      }
  
      // 更新藏品基本信息
      this.setData({
        collection: {
          id: mockCollectionData.id || collectionId,
          name: mockCollectionData.name || mockCollectionData.title || '',
          description: mockCollectionData.description || mockCollectionData.content || '',
          type: mockCollectionData.type || mockCollectionData.category || '',
          size: mockCollectionData.size || mockCollectionData.dimension || '',
          material: mockCollectionData.material || '',
          age: mockCollectionData.age || mockCollectionData.year || mockCollectionData.time || '',
          author: mockCollectionData.author || mockCollectionData.creator || '',
          collector: mockCollectionData.collector || mockCollectionData.museum || '',
          mediaList: mockCollectionData.mediaList || []
        },
        hasAudioMedia: hasAudioMedia,
        hasImageMedia: hasImageMedia,
        isLoading: false
      });
      
      // 更新藏品介绍显示
      this.updateIntroDisplay(mockCollectionData.description || mockCollectionData.content);
    } catch (error) {
      console.error('加载藏品详情失败:', error);
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
   * 点击图片全屏预览
   */
  previewImage: function(e) {
    const index = e.currentTarget.dataset.index;
    
    // 为每个图片URL添加static_url前缀
    // const fullUrls = images.map(image => this.data.static_url + image.mediaUrl);
    // this.data.collection.mediaList.map(image => if (image.type===1 || image.type===2) {
    //   url: this.data.static_url + image.url,
    // });
    // const media_src = {
    //   url: this.data.static_url + image.url,
    //   type: image.type===1?'image':'video',
    //   poster: this.data.static_url + image.url
    // };
    wx.previewMedia({
      sources: media_src,
      current: 0,
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