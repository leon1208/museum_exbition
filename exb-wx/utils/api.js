import config from '../config/index.js'

// API配置文件
const baseUrl = config.BASE_URL;
// 获取当前小程序的 app_id
const accountInfo = wx.getAccountInfoSync();
const appId = accountInfo.miniProgram.appId;

// API地址映射
export const apiUrls = {
  museum: {
    home: `${baseUrl}/wx/museum/home/${appId}`,
    exhibition_detail: `${baseUrl}/wx/museum/exhibition/detail/`  // 新增展览详情接口
    // 可以添加更多API地址
  }
};

// 封装wx.request方法
export const request = (url, method = 'GET', data = {}, header = {}) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url,
      method,
      data,
      header: {
        'content-type': 'application/json',
        ...header
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(new Error(`请求失败：${res.statusCode}`));
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
};

// 封装具体API请求方法
export const api = {
  // 获取博物馆首页数据
  getMuseumHomeData() {
    return request(apiUrls.museum.home);
  },
  // 获取展览详情数据
  getExhibitionDetail(exhibitionId) {
    return request(`${apiUrls.museum.exhibition_detail}${exhibitionId}`);
  }
  // 可以添加更多API方法
};