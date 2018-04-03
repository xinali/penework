/* router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
        if (store.state.token) {  // 通过vuex state获取当前的token是否存在
            next();
        }
        else {
            next({
                path: '/login',
                query: { redirect: to.fullPath }  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    }
    else {
        next();
    }
}); */

/*

loginRule: {
    username: [
      { required: true, message: "账号不能为空", trigger: 'blur' },
      { min: 3, max: 10, message: '长度在 3 到 16 个字符', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
    ],
  },
};

new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
*/

/* <el-table :data="projects" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="pid" width="60"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="120" sortable></el-table-column>
        <el-table-column prop="project_name" label="项目名称" width="120" sortable></el-table-column>
        <el-table-column prop="domain" label="域名" width="100" sortable></el-table-column>
        <el-table-column prop="status" label="状态" width="100" sortable></el-table-column>
        <el-table-column prop="description" label="描述" min-width="180" sortable></el-table-column>
        <el-table-column label="操作" width="150">
          <template scope="scope">
              <el-dropdown>
                <el-button type="primary">
                      详情<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
    						<el-dropdown-menu slot="dropdown">
    							<el-dropdown-item>端口信息</el-dropdown-item>
    							<el-dropdown-item>子域名信息</el-dropdown-item>
    							<el-dropdown-item>子目录信息</el-dropdown-item>
    						</el-dropdown-menu>
    					</el-dropdown>
              <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
  			</el-table-column>
          </el-table>*/
