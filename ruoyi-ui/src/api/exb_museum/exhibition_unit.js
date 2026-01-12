import request from '@/utils/request'


// 查询展览单元信息表列表
export function listExhibitionUnit(query) {
  return request({
    url: '/exb_museum/unit/list',
    method: 'get',
    params: query
  })
}

// 查询展览单元信息表详细
export function getExhibitionUnit(unitId) {
  return request({
    url: '/exb_museum/unit/' + unitId,
    method: 'get'
  })
}

// 新增展览单元信息表
export function addExhibitionUnit(data) {
  return request({
    url: '/exb_museum/unit',
    method: 'post',
    data: data
  })
}

// 修改展览单元信息表
export function updateExhibitionUnit(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/unit',
    method: 'put',
    data: data
  })
}

// 删除展览单元信息表
export function delExhibitionUnit(unitId) {
  return request({
    url: '/exb_museum/unit/' + unitId,
    method: 'delete'
  })
}