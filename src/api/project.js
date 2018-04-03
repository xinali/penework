import request from '@/utils/request'

const base = ''

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
export function editProject() {
  return request({
    url: `${base}/project/list`,
    method: 'post'
  })
}
export function addProject() {
  return request()
}
export function removeProject() {
  return request()
}
export function batchRemoveProject() {
  return request()
}
