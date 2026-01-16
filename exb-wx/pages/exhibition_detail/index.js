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
    sections: [], // 添加这个字段用于保存章节顺序
    groupedUnits: [], // 按section分组的展览单元
    collections: [], // 从展览单元中提取的主要展品
    showFullIntro: false,
    introText: '',
    // 新增音频相关数据
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
        const units = response.data.units || [];
        
        // 按section分组展览单元
        const groupedUnits = this.groupUnitsBySection(units, exhibitionData.sections);
        
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
            sections: exhibitionData.sections ? exhibitionData.sections.split(',') : [],
            coverImg: exhibitionData.coverImg || 'https://via.placeholder.com/400x300',
            galleryImages: exhibitionData.galleryImages || []
          },
          units: units,
          groupedUnits: groupedUnits,
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
            image: collection.imageUrl || collection.mediaList[0]?.url || '/wx_static/tmp_images/placeholder_image.png',
            hasAudio: collection.mediaList?.some(media => media.type === '2') || false, // 假设type为2表示音频
            description: collection.description || ''
          });
        });
      }
    });
    
    return collections;
  },

  /**
   * 按section分组展览单元
   */
  groupUnitsBySection: function(units, sections) {
    const grouped = {};
    
    units.forEach(unit => {
      const section = unit.section || '默认章节'; // 如果没有指定section，默认为"默认章节"
      
      if (!grouped[section]) {
        grouped[section] = [];
      }
      
      grouped[section].push(unit);
    });
    
    // 从sections中提取章节名称
    const sectionNames = sections? JSON.parse(sections).map(section => section.content) : ['默认章节'];
    const sorted_sections = sectionNames ? sectionNames : ['默认章节'];
    // 转换为数组格式便于wxml遍历
    const groupedArray = [];
    for (const idx in sorted_sections) {
      const section = sorted_sections[idx];
      groupedArray.push({
        sectionName: section,
        units: grouped[section]
      });
    }
    
    // 按section名称排序
    // groupedArray.sort((a, b) => a.sectionName.localeCompare(b.sectionName, 'zh-CN'));
    
    return groupedArray;
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
   * 查看展览单元详情
   */
  viewUnitDetail: function (e) {
    const dataset = e.currentTarget.dataset;
    const sectionIndex = dataset.sectionIndex;
    const unitIndex = dataset.index;
    
    // 从分组数据中获取对应单元
    const sectionUnits = this.data.groupedUnits[sectionIndex];
    if (!sectionUnits) return;
    
    const unit = sectionUnits.units[unitIndex];
    
    if (!unit) return;
    
    wx.navigateTo({
      url: `/pages/unit_detail/index?id=${unit.id}&name=${encodeURIComponent(unit.title || unit.name)}&description=${encodeURIComponent(unit.description || '')}`
    });
  },

  /**
   * 播放藏品音频
   */
  playUnitAudio: function (e) {
    const audioUrl = e.currentTarget.dataset.audioUrl;
    const audioName = e.currentTarget.dataset.audioName || '未知音频';
    
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
    
    // 创建内部 audio 上下文 InnerAudioContext 对象。
    const innerAudioContext = wx.createInnerAudioContext();

    // 关键配置：设置是否遵循系统静音开关，iOS静音模式下仍可播放
    innerAudioContext.autoplay = false
    innerAudioContext.loop = false
    innerAudioContext.obeyMuteSwitch = false;
    innerAudioContext.audioCategory = 'playback' 
    
    // 设置音频文件的路径
    innerAudioContext.src = audioUrl;
    
    // 监听音频播放事件
    innerAudioContext.onPlay(() => {
      console.log('音频开始播放');
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
      console.log('音频已暂停');
      this.setData({
        audioState: 'paused'
      });
    });
    
    // 监听音频停止事件
    innerAudioContext.onStop(() => {
      console.log('音频已停止');
      this.setData({
        audioState: 'stopped',
        currentAudioUrl: '',
        currentAudioName: ''
      });
    });
    
    // 监听音频播放结束事件
    innerAudioContext.onEnded(() => {
      console.log('音频播放结束');
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
      console.log('音频播放失败', res.errMsg, res.errCode);
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
   * 开始语音导览
   */
  startAudioGuide: function () {
    // 检查是否有正在进行的音频播放
    if (this.data.audioState === 'playing') {
      // 如果正在播放，则暂停
      if (this.data.audioContext) {
        this.data.audioContext.pause();
        this.setData({
          audioState: 'paused'
        });
        wx.showToast({
          title: '语音导览已暂停',
          icon: 'none'
        });
      }
      return;
    } else if (this.data.audioState === 'paused') {
      // 如果已暂停，则继续播放
      if (this.data.audioContext) {
        this.data.audioContext.play();
        this.setData({
          audioState: 'playing',
          currentAudioName: '语音导览' // 设置语音导览的名称
        });
        wx.showToast({
          title: '语音导览继续播放',
          icon: 'none'
        });
      }
      return;
    }
    
    // 如果是停止状态或没有音频在播放，开始新的语音导览
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
            
            // 在实际应用中，这里应该播放预设的语音导览音频
            // 设置语音导览的名称
            this.setData({
              currentAudioName: '语音导览'
            });
          }, 1500);
        }
      }
    });
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    // 销毁音频上下文，释放资源
    if (this.data.audioContext) {
      this.data.audioContext.destroy();
    }
  }
});