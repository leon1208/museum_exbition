// 展览详情页面逻辑
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
    exhibition: {
      id: '',
      title: '',
      description: '',
      startDate: '',
      endDate: '',
      organizer: '',
      hall: '',
      exhibitionType: '',
      contentTags: '',
      sections: '',
      coverImg: '',
      galleryImages: []
    },
    units: [],
    collections: [], // 从展览单元中提取的主要展品
    showFullIntro: false,
    introText: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取传递的展览ID参数
    // const exhibitionId = options.id || options.exhibition.id;
    const exhibition = JSON.parse(options.exhibition);
    const exhibitionId = exhibition.id
    
    if (!exhibitionId) {
      console.error('缺少展览ID参数');
      wx.showToast({
        title: '参数错误',
        icon: 'error'
      });
      return;
    }

    // 加载展览详情数据
    this.loadExhibitionDetail(exhibitionId);
  },

  /**
   * 更新展览介绍显示
   */
  updateIntroDisplay: function(description) {
    const maxLength = 100;
    let introText = '';
    
    if (description && description.length > maxLength) {
      introText = this.data.showFullIntro ? description : description.substring(0, maxLength) + '...';
    } else {
      introText = description || '暂无介绍';
    }
    
    this.setData({
      introText: introText
    });
  },

  /**
   * 加载展览详情数据
   */
  loadExhibitionDetail: async function(exhibitionId) {
    try {
      const response = await api.getExhibitionDetail(exhibitionId);
      
      if (response.code === 200) {
        const exhibitionData = response.data.exhibition;
        const units = response.data.units;
        
        // 更新展览基本信息
        this.setData({
          exhibition: {
            id: exhibitionData.id,
            title: exhibitionData.title || '',
            description: exhibitionData.description || '',
            startDate: exhibitionData.startDate || '',
            endDate: exhibitionData.endDate || '',
            organizer: exhibitionData.organizer || '',
            hall: exhibitionData.hall || '',
            exhibitionType: exhibitionData.exhibitionType || '',
            contentTags: exhibitionData.contentTags ? exhibitionData.contentTags.split(',') : [],
            sections: exhibitionData.sections || '',
            coverImg: exhibitionData.coverImg || 'https://via.placeholder.com/400x300',
            galleryImages: exhibitionData.galleryImages || []
          },
          units: units,
          collections: this.extractCollectionsFromUnits(units),
          isLoading: false
        });
        
        // 更新展览介绍显示
        this.updateIntroDisplay(exhibitionData.description);
      } else {
        throw new Error(response.msg || '获取展览详情失败');
      }
    } catch (error) {
      console.error('加载展览详情失败:', error);
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
   * 从展览单元中提取主要展品
   */
  extractCollectionsFromUnits: function(units) {
    const collections = [];
    
    units.forEach(unit => {
      if (unit.type === 0 && unit.collectionsDetail && Array.isArray(unit.collectionsDetail)) {
        // 展品单元类型，提取其中的藏品信息
        unit.collectionsDetail.forEach(collection => {
          collections.push({
            id: collection.id,
            name: collection.name,
            artist: collection.author || collection.material || '未知',
            image: collection.imageUrl || collection.mediaList[0]?.url || 'https://via.placeholder.com/200x200',
            hasAudio: collection.mediaList?.some(media => media.type === '2') || false, // 假设type为2表示音频
            description: collection.description || ''
          });
        });
      }
    });
    
    return collections;
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

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    // 重新加载当前展览详情
    const exhibitionId = this.data.exhibition.id;
    if (exhibitionId) {
      this.loadExhibitionDetail(exhibitionId);
      wx.stopPullDownRefresh();
    }
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    return {
      title: this.data.exhibition.title || '展览详情',
      path: `/pages/exhibition_detail/index?id=${this.data.exhibition.id}`
    };
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
   * 分享展览
   */
  shareExhibition: function () {
    // 触发分享，实际分享由 onShareAppMessage 处理
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  /**
   * 切换展览介绍显示状态
   */
  toggleIntro: function () {
    this.setData({
      showFullIntro: !this.data.showFullIntro
    });
    
    // 更新展览介绍显示
    this.updateIntroDisplay(this.data.exhibition.description);
  },

  /**
   * 查看展品详情
   */
  viewCollectionDetail: function (e) {
    const index = e.currentTarget.dataset.index;
    const collection = this.data.collections[index];
    
    if (!collection) return;
    
    wx.navigateTo({
      url: `/pages/collection_detail/index?id=${collection.id}&name=${encodeURIComponent(collection.name)}&artist=${encodeURIComponent(collection.artist)}`
    });
  },

  /**
   * 开始语音导览
   */
  startAudioGuide: function () {
    wx.showModal({
      title: '语音导览',
      content: '是否开始语音导览？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({
            title: '正在启动语音导览...',
            icon: 'loading'
          });
          
          // 模拟语音导览启动
          setTimeout(() => {
            wx.hideToast();
            wx.showToast({
              title: '语音导览已启动',
              icon: 'success'
            });
          }, 1500);
        }
      }
    });
  }
});