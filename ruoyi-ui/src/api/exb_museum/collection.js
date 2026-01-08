import request from '@/utils/request'


// 查询藏品信息表列表
export function listCollection(query) {
  return request({
    url: '/exb_museum/collection/list',
    method: 'get',
    params: query
  })
}

// 查询藏品信息表详细
export function getCollection(collectionId) {
  return request({
    url: '/exb_museum/collection/' +collectionId,
    method: 'get'
  })
}

// 新增藏品信息表
export function addCollection(data) {
  return request({
    url: '/exb_museum/collection',
    method: 'post',
    data: data
  })
}

// 修改藏品信息表
export function updateCollection(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/collection',
    method: 'put',
    data: data
  })
}

// 删除藏品信息表
export function delCollection(collectionId) {
  return request({
    url: '/exb_museum/collection/' +collectionId,
    method: 'delete'
  })
}