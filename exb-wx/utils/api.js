import config from '../config/index.js'
import sha256 from './sha256.js'


// API配置文件
const baseUrl = config.BASE_URL;
// 获取当前小程序的 app_id
const accountInfo = wx.getAccountInfoSync();
const appId = accountInfo.miniProgram.appId;

// API地址映射
export const apiUrls = {
  museum: {
    home: `${baseUrl}/wx/museum/home/${appId}`,
    exhibition_detail: `${baseUrl}/wx/museum/exhibition/detail/`,  // 新增展览详情接口
    unit_detail: `${baseUrl}/wx/museum/exhibition/unit/detail/`  // 新增展览单元详情接口
    // 可以添加更多API地址
  },
  auth: {
    login: `${baseUrl}/wx/auth/login`,
    refresh: `${baseUrl}/wx/auth/refresh`  // 可能需要的刷新接口
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

// 封装带认证的请求方法
export const authenticatedRequest = (url, method = 'GET', data = {}, customHeader = {}) => {
  const token = wx.getStorageSync('access_token');
  const timestamp = Math.floor(Date.now() / 1000)
  const nonce = Math.random().toString(36).slice(2, 12)
  const path = url.substring(baseUrl.length)
  const bodyStr = data && Object.keys(data).length !== 0 ? JSON.stringify(data) : ''

  const signStr = [
    method.toUpperCase(),
    path,
    bodyStr,
    timestamp,
    nonce,
    token
  ].join('\n')
  const sign = sha256(signStr)
  
  const header = {
    'Authorization': `Bearer ${token}`,
    'content-type': 'application/json',
    'X-Timestamp': timestamp,
    'X-Nonce': nonce,
    'X-Sign': sign,
    ...customHeader
  };  

  return request(url, method, data, header);
};

// 封装具体API请求方法
export const api = {
  // 获取博物馆首页数据
  getMuseumHomeData() {
    return authenticatedRequest(apiUrls.museum.home);
  },
  // 获取展览详情数据
  getExhibitionDetail(exhibitionId) {
    return authenticatedRequest(`${apiUrls.museum.exhibition_detail}${exhibitionId}`);
  },
  // 获取展览单元详情数据
  getUnitDetail(unitId) {
    return authenticatedRequest(`${apiUrls.museum.unit_detail}${unitId}`);
  },
  // 微信登录
  login(code) {
    return request(apiUrls.auth.login, 'POST', { 
      code: code,
      app_id: appId 
    });
  },
  // 刷新用户信息
  refreshToken() {
    const token = wx.getStorageSync('access_token');
    return request(apiUrls.auth.refresh, 'POST', { 
      access_token: token,
      app_id: appId 
    });
  }
  // 可以添加更多API方法
};