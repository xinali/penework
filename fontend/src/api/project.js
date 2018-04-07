import request from '@/utils/request'

const base = 'api'

/*
parmas:
  page: page_num
  filter.project_name // for search
*/
export function getProjectListPage(params) {
  return request({
    url: '/project/list',
    method: 'get',
    params: params
  })
}
export function editProject(params) {
  return request({
    url: `${base}/project/update`,
    method: 'post',
    params
  })
}
export function addProject(params) {
  return request({
    url: `${base}/project/add`,
    method: 'post',
    params
  })
}
export function removeProject(params) {
  return request({
    url: '/project/remove',
    method: 'get',
    params: params
  })
}
export function batchRemoveProject(params) {
  return request({
    url: `${base}/project/removes`,
    method: 'post',
    params
  })
}
