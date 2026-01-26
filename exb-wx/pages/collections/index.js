// 引入API工具
import { api } from '../../utils/api.js';
import config from '../../config/index.js';

Page({
  data: {
    museumId: null, // 博物馆ID
    selectedCategory: '全部', // 当前选中的分类
    categories: ['全部', '民国', '明清', '艺术', '瓷器', '国画', '书法', '青铜器', '玉器', '珠宝', '钱币', '文房四宝', '家具'], // 动态标签数组
    collections: [], // 所有展品数据
    filteredCollections: [], // 筛选后的展品数据
    isLoading: false, // 是否正在加载
    hasMore: false, // 是否还有更多数据
    // page: 1, // 当前页码
    // pageSize: 20, // 每页数量
    static_url: config.STATIC_URL // 静态资源地址
  },

  onLoad: function (options) {
    // 页面加载时请求数据
    const museumId = options.museumId;
    if (!museumId) {
      console.error('博物馆ID参数缺失');
      return;
    }

    this.setData({
      museumId: museumId
    });

    // 等待登录完成后加载数据
    const app = getApp();
    app.waitForLogin(() => {
      this.loadCollections();
    });
  },

  /**
   * 分类标签点击事件
   */
  onCategoryTap: function (e) {
    const category = e.currentTarget.dataset.category;
    if (this.data.selectedCategory !== category) {
      this.setData({
        selectedCategory: category
      });
      
      // 根据分类筛选数据，而不是重新加载
      this.applyFilter();
    }
  },

  /**
   * 应用筛选条件
   */
  applyFilter: function () {
    const { collections, selectedCategory } = this.data;
    
    if (selectedCategory === '全部') {
      this.setData({
        filteredCollections: collections
      });
      return;
    }
    
    const filtered = collections.filter(item => {
      // 检查藏品的type、age、material等属性是否匹配筛选条件
      return (
        (item.type && item.type.includes(selectedCategory)) ||
        (item.age && item.age.includes(selectedCategory)) ||
        (item.material && item.material.includes(selectedCategory))
      );
    });
    
    this.setData({
      filteredCollections: filtered
    });
  },

  /**
   * 加载展品数据
   */
  loadCollections: function () {
    if (this.data.isLoading) {
      return;
    }

    this.setData({
      isLoading: true
    });

    // 调用API获取展品列表
    api.getCollections(this.data.museumId)
      .then(res => {
        if (res.code === 200) {
          const newCollections = res.data || [];
          
          // 更新所有展品数据
          // const updatedCollections = [...newCollections, ...newCollections];
          const updatedCollections = [...newCollections]
          
          this.setData({
            collections: updatedCollections,
            // 初始时显示所有数据
            filteredCollections: updatedCollections,
            isLoading: false,
            // hasMore: newCollections.length === this.data.pageSize // 如果返回的数量等于每页数量，说明可能还有更多
            hasMore: false,
          });
        } else {
          console.error('获取展品列表失败:', res.msg || '未知错误');
          this.setData({
            isLoading: false
          });
        }
      })
      .catch(err => {
        console.error('获取展品列表出错:', err);
        this.setData({
          isLoading: false
        });
      });
  },

  /**
   * 滚动到底部事件 - 加载更多数据
   */
  onScrollToLower: function () {
    if (!this.data.isLoading && this.data.hasMore) {
      this.setData({
        // page: this.data.page + 1
      });
      this.loadCollections();
    }
  },

  /**
   * 展品点击事件
   */
  onCollectionTap: function (e) {
    const collection = e.currentTarget.dataset.collection;
    // 跳转到藏品详情页面
    wx.navigateTo({
      url: '../collection_detail/index?collection=' + JSON.stringify(collection)
    });
  },

  /**
   * 返回上一页
   */
  goBack: function () {
    wx.navigateBack();
  },
});