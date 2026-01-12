import request from '@/utils/request'


// 查询展厅信息表列表
export function listMuseumHall(query) {
  return request({
    url: '/exb_museum/hall/list',
    method: 'get',
    params: query
  })
}

// 查询展厅信息表详细
export function getMuseumHall(hallId) {
  return request({
    url: '/exb_museum/hall/' + hallId,
    method: 'get'
  })
}

// 新增展厅信息表
export function addMuseumHall(data) {
  return request({
    url: '/exb_museum/hall',
    method: 'post',
    data: data
  })
}

// 修改展厅信息表
export function updateMuseumHall(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/hall',
    method: 'put',
    data: data
  })
}

// 删除展厅信息表
export function delMuseumHall(hallId) {
  return request({
    url: '/exb_museum/hall/' + hallId,
    method: 'delete'
  })
}