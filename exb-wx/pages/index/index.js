// index.js
// const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'

// 引入API工具
import { api } from '../../utils/api.js';
import config from '../../config/index.js'

// index.js
Page({
  data: {
    museum: {}, // 博物馆基本信息
    collections: [], // 馆藏精选
    exhibitions: [], // 展览信息
    educations: [], // 教育活动
    tabIndex: 0,
    static_url: config.STATIC_URL //静态资源地址
  },

  onLoad: function () {
    // 页面加载时请求数据
    this.getMuseumData();
  },

  // 加载博物馆数据
   async getMuseumData() {
    try {
      const res = await api.getMuseumHomeData();
      if (res.code === 200) {
        this.setData({
          museum: res.data.museum,
          collections: res.data.collections,
          exhibitions: res.data.exhibitions,
          educations: res.data.educations
        });
      }
    } catch (err) {
      console.error('请求博物馆数据失败:', err);
      // 失败时使用默认数据
      this.setDefaultData();
    }
  },

  // 设置默认数据
  setDefaultData: function () {
    this.setData({
      museum: {
        name: '国家历史博物馆',
        description: '探索数千年的人类文化遗产，从古代珍贵文物到现代艺术杰作，尽在其中。',
        openStatus: '今日开放',
        openTime: '09:00 - 17:00',
        bgImage: '/wx_static/tmp_images/bg1.png'
      },
      collections: [
        {
          title: '明代青花瓷',
          period: '明朝',
          img: '/wx_static/tmp_images/it01.png'
        },
        {
          title: '皇家金冠',
          period: '18世纪',
          img: '/wx_static/tmp_images/it02.png'
        },
        {
          title: '青铜短剑',
          period: '青铜时代',
          img: '/wx_static/tmp_images/it03.png' 
        }
      ],
      exhibitions: [
        {
          title: '2024 现代艺术展',
          desc: '一场当代表现主义的探索之旅。',
          date: '10月12日 - 12月30日',
          place: '二层 A厅',
          status: 'hot',
          statusText: '正在热展',
          img: '/wx_static/tmp_images/exb01.png'
        },
        {
          title: '罗马帝国的荣耀',
          desc: '探索塑造世界的伟大帝国。',
          date: '1月10日 - 3月15日',
          place: '中央大厅',
          status: 'upcoming',
          statusText: '即将开展',
          img: '/wx_static/tmp_images/exb02.png'
        }
      ],
      educations: [
        {
          type: '工作坊',
          title: '陶艺体验大师课',
          time: '明日 10:00',
          img: '/wx_static/tmp_images/act01.png'
        },
        {
          type: '讲座',
          title: '策展人视角导览',
          time: '周日 14:00',
          img: '/wx_static/tmp_images/act02.png'
        }
      ]
    });
  },

  // 切换标签
  switchTab: function (e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      tabIndex: index
    });
  },

  // Swiper 滑动事件
  onSwiperChange(e) {
    this.setData({
      swiperCurrent: e.detail.current
    });
  },
  
  //以下暂时无用
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onChooseAvatar(e) {
    const { avatarUrl } = e.detail
    const { nickName } = this.data.userInfo
    this.setData({
      "userInfo.avatarUrl": avatarUrl,
      hasUserInfo: nickName && avatarUrl && avatarUrl !== defaultAvatarUrl,
    })
  },
  onInputChange(e) {
    const nickName = e.detail.value
    const { avatarUrl } = this.data.userInfo
    this.setData({
      "userInfo.nickName": nickName,
      hasUserInfo: nickName && avatarUrl && avatarUrl !== defaultAvatarUrl,
    })
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
})