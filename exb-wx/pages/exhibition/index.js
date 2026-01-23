// 展览列表页面逻辑
import { api } from '../../utils/api.js';
import config from '../../config/index.js';

Page({
  /**
   * 页面的初始数据
   */
  data: {
    museumId: null,
    exhibitions: [],
    filteredExhibitions: [],
    currentFilter: '全部',
    static_url: config.STATIC_URL,
    isLoading: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    const museumId = options.museumId || 8;
    this.setData({
      museumId: museumId
    });

    // 加载展览列表数据
    this.loadExhibitions();
  },

  /**
   * 加载展览列表数据
   */
  loadExhibitions: async function () {
    try {
      this.setData({
        isLoading: true
      });
  
      // 调用API获取展览列表
      const response = await api.getExhibitions(this.data.museumId);
  
      if (response.code === 200) {
        let exhibitions = response.data || [];
        
        // 将contentTags转换为数组
        exhibitions = exhibitions.map(item => {
          item.contentTagsArray = item.contentTags 
            ? item.contentTags.split(',').map(tag => tag.trim()) 
            : ['展览'];
          return item;
        });
        
        // 设置展览数据并应用当前筛选条件
        this.setData({
          exhibitions: exhibitions,
          filteredExhibitions: this.applyFilter(exhibitions, this.data.currentFilter),
          isLoading: false
        });
      } else {
        throw new Error(response.msg || '获取展览列表失败');
      }
    } catch (error) {
      console.error('加载展览列表失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'error'
      });
      
      // 设置空数组避免页面报错
      this.setData({
        exhibitions: [],
        filteredExhibitions: [],
        isLoading: false
      });
    }
  },

  /**
   * 应用筛选条件
   */
  applyFilter: function (exhibitions, filter) {
    if (filter === '全部') {
      return exhibitions;
    }
    
    return exhibitions.filter(item => {
      // 检查展览类型或分类是否匹配筛选条件
      return (
        (item.contentTags && item.contentTags.includes(filter)) ||
        (item.exhibitionType && item.exhibitionType.includes(filter))
      );
    });
  },

  /**
   * 更改筛选条件
   */
  changeFilter: function (event) {
    const filter = event.currentTarget.dataset.filter;
    
    this.setData({
      currentFilter: filter,
      filteredExhibitions: this.applyFilter(this.data.exhibitions, filter)
    });
  },

  /**
   * 查看展览详情
   */
  viewExhibitionDetail: function (event) {
    const exhibition = event.currentTarget.dataset.exhibition;
    // 跳转到展览详情页面
    wx.navigateTo({
      // url: `/pages/exhibition_detail/index?exhibition=${encodeURIComponent(JSON.stringify(exhibition))}`
      url: '../exhibition_detail/index?exhibition=' + JSON.stringify(exhibition)
    });
  },

  /**
   * 返回上一页
   */
  goBack: function () {
    wx.navigateBack();
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh: function () {
    this.loadExhibitions().then(() => {
      wx.stopPullDownRefresh();
    });
  }
});