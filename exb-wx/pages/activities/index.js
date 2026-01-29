// 教育活动列表页面逻辑
import { api } from '../../utils/api.js';
import config from '../../config/index.js';

Page({
  /**
   * 页面的初始数据
   */
  data: {
    museumId: null,
    educations: [],
    filteredEducations: [],
    currentFilter: '全部',
    filters: ['全部', '讲座', '手工', '表演', '其他'],
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

    // 加载教育活动列表数据
    this.loadEducations();
  },

  /**
   * 加载教育活动列表数据
   */
  loadEducations: async function () {
    try {
      this.setData({
        isLoading: true
      });
  
      // 调用API获取教育活动列表
      const response = await api.getEducations(this.data.museumId);
  
      if (response.code === 200) {
        let educations = response.data || [];
        
        // 格式化时间显示
        educations = educations.map(item => {
          // 格式化时间显示
          if (!item.time) {
            item.time = `${item.startTime || ''} - ${item.endTime || ''}`;
          }
          return item;
        });
        
        // 设置教育活动数据并应用当前筛选条件
        this.setData({
          educations: educations,
          filteredEducations: this.applyFilter(educations, this.data.currentFilter),
          isLoading: false
        });
      } else {
        throw new Error(response.msg || '获取教育活动列表失败');
      }
    } catch (error) {
      console.error('加载教育活动列表失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'error'
      });
      
      // 设置空数组避免页面报错
      this.setData({
        educations: [],
        filteredEducations: [],
        isLoading: false
      });
    }
  },

  /**
   * 应用筛选条件
   */
  applyFilter: function (educations, filter) {
    if (filter === '全部') {
      return educations;
    }
    
    return educations.filter(item => {
      // 检查活动类型是否匹配筛选条件
      return (
        (item.type && item.type.includes(filter)) ||
        (item.activity_type && item.activity_type.includes(filter))
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
      filteredEducations: this.applyFilter(this.data.educations, filter)
    });
  },

  /**
   * 查看教育活动详情
   */
  viewEducationDetail: function (event) {
    const education = event.currentTarget.dataset.education;
    // 跳转到教育活动详情页面
    wx.navigateTo({
      url: '../activity_detail/index?activity=' + JSON.stringify(education)
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
    this.loadEducations().then(() => {
      wx.stopPullDownRefresh();
    });
  }
});
