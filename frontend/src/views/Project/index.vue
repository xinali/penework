<template>
  <section>
    <!--工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" :model="filters">
        <el-form-item>
          <el-input :model="filters.project_name" placeholder="项目"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getProjectList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table :data="projects" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
       <el-table-column type="selection" width="55"></el-table-column>
      <!-- <el-table-column v-for="{ prop, label, width } in ShowConfigs" :key="prop" :prop="prop" :label="label" :width="width"> -->
      <el-table-column v-for="{ prop, label } in ShowConfigs" :key="prop" :prop="prop" :label="label">
      </el-table-column>
      <el-table-column label="操作" width="250">
          <template slot-scope="scope">
              <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
              <el-dropdown>
                <!-- <el-button type="primary"> -->
                <el-button size="small">
                      详情<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
    						<el-dropdown-menu slot="dropdown">
    							<el-dropdown-item @click="getPortInfo(scope.$index, scope.row)">端口信息</el-dropdown-item>
    							<el-dropdown-item @click="getSubDomain(scope.$index, scope.row)">子域名信息</el-dropdown-item>
    							<!-- <el-dropdown-item @click="getDirs>子目录信息</el-dropdown-item> -->
    						</el-dropdown-menu>
    					</el-dropdown>
          </template>
  			</el-table-column>
    </el-table>

    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
      <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
      </el-pagination>
    </el-col>
    
    <!--编辑界面-->
    <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
      <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="editForm.project_name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="域名" prop="domain">
          <el-input v-model="editForm.domain" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="editForm.description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--新增界面-->
    <el-dialog title="新增项目" :visible.sync="addFormVisible" :close-on-click-modal="false" >
      <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="项目名称">
          <el-input v-model="addForm.project_name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="域名">
          <el-input v-model="addForm.domain" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="addForm.description"></el-input>
        </el-form-item>

        <el-collapse v-model="addForm.activeName" accordion>
          <el-collapse-item title="扫描配置" name="1">
            <el-form-item label="扫描端口">
              <el-input type="textarea" v-model="addForm.scan_ports"></el-input>
            </el-form-item>
            <el-form-item label="扫描范围">
              <el-input type="textarea" v-model="addForm.scan_ip_range"></el-input>
            </el-form-item>
            <el-form-item label="扫描频率">
              <el-input v-model="addForm.scan_frequency"></el-input>
            </el-form-item>
            <el-form-item label="扫描方式">
              <el-radio-group v-model="addForm.radio2_select_ways">
                <el-radio :label="3">masscan</el-radio>
                <el-radio :label="6">nasscan</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-collapse-item>
          <el-collapse-item title="爬虫配置" name="2">
            <div>爬虫设置</div>
          </el-collapse-item>
        </el-collapse>

      </el-form>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
      </div>
    </el-dialog>

  </section>
</template>

<script>
  import {
    getProjectListPage,
    removeProject,
    batchRemoveProject,
    editProject,
    addProject
  } from '@/api/project'

  export default {
    data() {
      this.ShowConfigs = [
        { prop: 'pid', label: 'id', width: 60 },
        { prop: 'create_time', label: '创建时间', width: 100 },
        { prop: 'project_name', label: '项目名称', width: 100 },
        { prop: 'domain', label: '域名', width: 80 },
        { prop: 'status', label: '状态', width: 50 },
        { prop: 'description', label: '描述', width: 120 }
      ]
      return {
        filters: {
          project_name: ''
        },
        total: 0,
        page: 1,
        listLoading: false,
        sels: [], // 列表选中列
        projects: [],

        editFormVisible: false, // 编辑界面是否显示
        editLoading: false,
        // 编辑界面数据
        editForm: {
          pid: 0,
          project_name: '',
          domain: '',
          description: ''
        },
        editFormRules: {
          project_name: [{
            required: true,
            message: '请输入项目',
            trigger: 'blur'
          }]
        },

        addFormVisible: false,
        addLoading: false,
        // 新增界面数据
        addForm: {
          pid: 0,
          project_name: '',
          domain: '',
          description: '',
          radio2_select_ways: 3,
          scan_ports: [],
          scan_ip_range: '',
          scan_frequency: '',
          activeName: ['1']
        },
        addFormRules: {
          project_name: [{
            required: true,
            message: '请输入项目',
            trigger: 'blur'
          }]
        }
      }
    },
    methods: {
      handleCurrentChange(val) {
        this.page = val
        this.getProjectList()
      },
      // 获取项目列表
      getProjectList() {
        const para = {
          page: this.page
        }
        this.listLoading = true
        getProjectListPage(para).then((res) => {
          this.total = res.data.total
          this.projects = res.data.projects
          this.listLoading = false
        })
      },
      // 删除
      handleDel: function(index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true
          const para = {
            pid: row.pid
          }
          removeProject(para).then((res) => {
            this.listLoading = false
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getProjectProject()
          })
        }).catch(() => {})
      },
      // 显示编辑界面
      handleEdit: function(index, row) {
        this.editFormVisible = true
        this.editForm = Object.assign({}, row)
      },
      // 编辑
      editSubmit: function() {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true
              const para = Object.assign({}, this.editForm)
              editProject(para).then((res) => {
                this.editLoading = false
                this.$message({
                  message: '提交成功',
                  type: 'success'
                })
                this.$refs['editForm'].resetFields()
                this.editFormVisible = false
                this.getProjectList()
              })
            })
          }
        })
      },
      // 显示新增界面
      handleAdd: function() {
        this.addFormVisible = true
        this.addForm = {
          pid: 0,
          project_name: '',
          domain: '',
          description: ''
        }
        console.log('Execute handleAdd completely....')
      },
      // 新增
      addSubmit: function() {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addLoading = true
              const para = Object.assign({}, this.addForm)
              addProject(para).then((res) => {
                this.addLoading = false
                this.$message({
                  message: '提交成功',
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
                this.getProjectList()
              })
            })
          }
        })
      },
      selsChange: function(sels) {
        this.sels = sels
      },
      // 批量删除
      batchRemove: function() {
        var ids = this.sels.map(item => item.id).toString()
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true
          const para = {
            ids: ids
          }
          batchRemoveProject(para).then((res) => {
            this.listLoading = false
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getProjectList()
          })
        }).catch(() => {})
      }
    },
    mounted() {
      this.getProjectList()
    }
  }
</script>