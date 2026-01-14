// 展览详情页面逻辑
Page({
  /**
   * 页面的初始数据
   */
  data: {
    scrollTop: 0,
    showTitle: false,
    isFavorite: false,
    introText: '本次展览汇集了15世纪至16世纪文艺复兴时期的众多杰作，旨在探索那个时代艺术、科学与人文精神的辉煌交汇。观众将有机会近距离欣赏到包括达·芬奇、米开朗基罗等大师的真迹手稿与经典油画...',
    fullIntroText: '本次展览汇集了15世纪至16世纪文艺复兴时期的众多杰作，旨在探索那个时代艺术、科学与人文精神的辉煌交汇。观众将有机会近距离欣赏到包括达·芬奇、米开朗基罗等大师的真迹手稿与经典油画，感受那个时代无与伦比的艺术成就。展览通过精心策划的展示路径，引导观众穿越时空，体验文艺复兴时期的人文主义精神与创新理念。展品涵盖了绘画、雕塑、手稿等多个艺术门类，全面展现了文艺复兴时期艺术的多样性与深度。',
    showFullIntro: false,
    isLoading: true,
    collections: [
      {
        name: "蒙娜丽莎",
        artist: "列奥纳多·达·芬奇",
        image: "https://wp1.telecomsh.cn/minio/museum/media/2026/01/14/135ab02fbb7b43b38e7e298d38729516.JPG",
        hasAudio: true
      },
      {
        name: "大卫像",
        artist: "米开朗基罗",
        image: "https://wp1.telecomsh.cn/minio/museum/media/2026/01/14/3fb9ac26173b428ab49113cb431356c4.JPG",
        hasAudio: false
      },
      {
        name: "维特鲁威人",
        artist: "列奥纳多·达·芬奇",
        image: "https://wp1.telecomsh.cn/minio/museum/media/2026/01/14/275ae8a4675c49cea53bd8e3b450d6e7.JPG",
        hasAudio: true
      },
      {
        name: "维纳斯的诞生",
        artist: "波提切利",
        image: "https://wp1.telecomsh.cn/minio/museum/media/2026/01/14/275ae8a4675c49cea53bd8e3b450d6e7.JPG",
        hasAudio: false
      },
      {
        name: "最后的晚餐",
        artist: "列奥纳多·达·芬奇",
        image: "https://wp1.telecomsh.cn/minio/museum/media/2026/01/14/135ab02fbb7b43b38e7e298d38729516.JPG",
        hasAudio: false
      },
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 模拟加载数据
    setTimeout(() => {
      this.setData({
        isLoading: false
      });
    }, 1500);
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
      title: '文艺复兴：伟大的大师们',
      path: '/pages/exhibition_detail/index'
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
  },

  /**
   * 查看展品详情
   */
  viewCollectionDetail: function (e) {
    const index = e.currentTarget.dataset.index;
    const collection = this.data.collections[index];
    
    wx.navigateTo({
      url: `/pages/collection_detail/index?name=${encodeURIComponent(collection.name)}&artist=${encodeURIComponent(collection.artist)}`
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