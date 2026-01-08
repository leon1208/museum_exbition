import request from '@/utils/request'


// 查询展览信息表列表
export function listExbition(query) {
  return request({
    url: '/exb_museum/exbition/list',
    method: 'get',
    params: query
  })
}

// 查询展览信息表详细
export function getExbition(exhibitionId) {
  return request({
    url: '/exb_museum/exbition/' +exhibitionId,
    method: 'get'
  })
}

// 新增展览信息表
export function addExbition(data) {
  return request({
    url: '/exb_museum/exbition',
    method: 'post',
    data: data
  })
}

// 修改展览信息表
export function updateExbition(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/exbition',
    method: 'put',
    data: data
  })
}

// 删除展览信息表
export function delExbition(exhibitionId) {
  return request({
    url: '/exb_museum/exbition/' +exhibitionId,
    method: 'delete'
  })
}