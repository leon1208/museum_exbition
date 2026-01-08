import request from '@/utils/request'


// 查询展览信息表列表
export function listExhibition(query) {
  return request({
    url: '/exb_museum/exhibition/list',
    method: 'get',
    params: query
  })
}

// 查询展览信息表详细
export function getExhibition(exhibitionId) {
  return request({
    url: '/exb_museum/exhibition/' +exhibitionId,
    method: 'get'
  })
}

// 新增展览信息表
export function addExhibition(data) {
  return request({
    url: '/exb_museum/exhibition',
    method: 'post',
    data: data
  })
}

// 修改展览信息表
export function updateExhibition(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/exhibition',
    method: 'put',
    data: data
  })
}

// 删除展览信息表
export function delExhibition(exhibitionId) {
  return request({
    url: '/exb_museum/exhibition/' +exhibitionId,
    method: 'delete'
  })
}