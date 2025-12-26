import request from '@/utils/request'





// 查询博物馆信息表列表
export function listMuseum(query) {
  return request({
    url: '/exb_museum/museum/list',
    method: 'get',
    params: query
  })
}

// 查询博物馆信息表详细
export function getMuseum(museumId) {
  return request({
    url: '/exb_museum/museum/' +museumId,
    method: 'get'
  })
}

// 新增博物馆信息表
export function addMuseum(data) {
  return request({
    url: '/exb_museum/museum',
    method: 'post',
    data: data
  })
}

// 修改博物馆信息表
export function updateMuseum(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/museum',
    method: 'put',
    data: data
  })
}

// 删除博物馆信息表
export function delMuseum(museumId) {
  return request({
    url: '/exb_museum/museum/' +museumId,
    method: 'delete'
  })
}