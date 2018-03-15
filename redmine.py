from jira import JIRA
import requests
import os
import logging
import logging.config

def redmine(id):
    url = 'http://10.10.80.228/redmine/issues/'+ str(id) +'.json'
    params = {'include': 'attachments,journals,changesets'}
    r=requests.get(url,params)
    r_js = r.json()
    return r_js
#下载附件
def downlond(dirname,filename,url):
    dirname=str(dirname)
    path = os.path.abspath(os.curdir)+'\\redmine\\'+dirname
    if os.path.isdir(path) :
        pass
    else:
        os.mkdir(path)
    r = requests.get(url)

    with open(path+'/'+filename, "wb") as code:
        code.write(r.content)
    logger.info("下载"+dirname+"附件")
#获取rendmine任务信息
def dictget(re_issue):
    redmine={}
    for k,v in re_issue.items():
        if k=="custom_fields":
            cus = re_issue['custom_fields']
            for k1 in cus:
                name = k1['name']
                if 'value' in k1.keys():
                    value = k1['value']
                else:
                    value =''
                redmine[name] = value

            logger.info('获取redmine：'+str(re_issue['id'])+'自定义字段信息')

        elif k=='journals':
            journals={}
            cus=re_issue['journals']
            for k1 in cus:
                if 'notes' in k1.keys():
                    if k1['notes'] != "":
                        author = k1['user']['name']
                        notes=k1['notes']
                        create_on=k1['created_on']
                        journals[create_on+author]= notes
                        redmine['备注']=journals
            logger.info('获取redmine：' + str(re_issue['id']) + '历史操作信息')

        elif k=='attachments':
            id=re_issue['id']
            attachments={}
            att=re_issue['attachments']
            for k2 in att:
                name=k2['filename']
                url=k2['content_url']
                attachments[name]=url
                redmine['附件']=attachments
                downlond(id,name,url)

            logger.info('获取redmine：' + str(re_issue['id']) + '附件信息')


        else:
            if type(v) is dict:
                if 'name' in v:
                    redmine[k]=v['name']
                else:
                    redmine[k]=v
            else:
                redmine[k]=v
    return redmine
#添加附件

#修改ite-packages/requests/packages/urllib3/fields.py, 第38行
#     result = '%s="%s"' % (name, value)
#     try:
#         result.encode('utf-8') 将result.encode('ascii')修改为utf-8
#     except UnicodeEncodeError:
#         pass
#     else:
#         return result
def add_attachment(issuekey, re_issue):
    path=os.path.abspath(os.curdir)+'\\redmine\\'+str(re_issue['id'])

    if os.path.isdir(path):
        pathDir=os.listdir(path)
        for filename in pathDir:
            s = path + '\\' + filename
            jira.add_attachment(issuekey,s)

            logger.info("添加："+str(issuekey)+"附件"+filename+"##redmine标号:" + str(re_issue['id']))
    else:
        logger.info("添加：" + str(issuekey) + "附件.##redmine标号："+ str(re_issue['id']))
        pass
#添加备注
def add_comment(issuekey,re_issue):
    comment=re_issue['备注']
    s = sorted(comment.items(), key=lambda dict: dict[0], reverse=True)
    for i in range(0, len(s)):
        jira.add_comment(issuekey, s[i][0] + '\r\n' + s[i][1])

    # date=str(re_issue['date'])[1:-1]

    # jira.add_comment(issuekey, date)
    # # logger.info("添加：" + str(issuekey) + "日期备注.##redmine标号：" + str(re_issue['id']))
    # for k,v in comment.items():
    #     if v is not None:
    #         jira.add_comment(issuekey, str(k)+'\r\n '+str(v))
    logger.info("添加：" + str(issuekey) + "附件.##redmine标号：" + str(re_issue['id']))


#字段转换
def change(re,filename):
    if re['priority'] is not None:
        if re['priority']=='立刻':
            re['priority']='Blocker'

        elif re['priority']=='紧急':
            re['priority']='Critical'

        elif re['priority']=='高':
            re['priority']='Major'

        elif re['priority']=='普通':
            re['priority']='Minor'

        elif re['priority']=='低':
            re['priority']='Trivial'

        logger.info("转换：" + str(re['id']) + "优先级字段.")
    else:
        logger.info("编号：" + str(re['id']) + "无优先级字段.")

    if '缺陷归因' in  re.keys():
        if re['priority'] is not None:
            if re['缺陷归因']=='流程/标准缺陷':
                re['缺陷归因'] = '其他'

            elif re['缺陷归因']=='需求变更':
                re['缺陷归因'] = '需求分析'

            elif re['缺陷归因']=='用例设计':
                re['缺陷归因'] = '测试设计'
            logger.info("转换：" + str(re['id']) + "缺陷归因.")
        else:
            logger.info("编号：" + str(re['id']) + "无缺陷归因.")
    else:
        logger.info("编号：" + str(re['id']) + "无缺陷归因字段.")

    if '测试环境' in  re.keys():
        if re['测试环境'] is not None:
            if re['测试环境']=='SIT测试环境':
                re['测试环境'] = '测试环境'

            elif re['测试环境']=='UAT测试环境':
                re['测试环境'] = 'UAT环境'

            elif re['测试环境']=='dev测试环境':
                re['测试环境'] = '开发环境'

            logger.info("转换：" + str(re['id']) + "测试环境.")
        else:
            logger.info("编号：" + str(re['id']) + "无测试环境.")
    else:
        logger.info("编号：" + str(re['id']) + "无测试环境字段.")

    if '测试周期' in  re.keys():
        if re['测试周期'] is not None:
            if re['测试周期']=='SIT测试第一轮':
                re['测试周期'] = '系统测试-第一轮'

            elif re['测试周期']=='SIT测试第二轮':
                re['测试周期'] = '系统测试-第二轮'

            elif re['测试周期']=='SIT测试第三轮':
                re['测试周期'] = '系统测试-第三轮'
            logger.info("转换：" + str(re['id']) + "测试周期.")
        else:
            logger.info("编号：" + str(re['id']) + "无测试周期.")
    else:
        logger.info("编号：" + str(re['id']) + "无测试周期字段.")

    for k,v in re.items():
        if v == '':
            re[k]=None

        if k == '需求确认计划耗时（人天）' or k == '开发计划耗时（人天）' or k == 'UAT测试计划耗时（人天）':
            if re[k] is not None:
                re[k] = float(v)

    # if 'start_date' in re.keys():
    #     date={'开始日期':re['start_date']}
    #     if 'due_date' in re.keys():
    #         key='计划完成日期'
    #         value=re['due_date']
    #         date[key]=value
    #         re.pop('due_date')
    #         logger.info("编号：" + str(re['id']) + "添加计划日期到date字典中.")
    #
    #     if 'estimated_hours' in re.keys():
    #         key='预期时间'
    #         value=re['estimated_hours']
    #         date[key]=value
    #         re.pop('estimated_hours')
    #         logger.info("编号：" + str(re['id']) + "预期时间到date字典中.")
    #
    #     if 'closed_on' in re.keys():
    #         key='结束时间'
    #         value=re['closed_on']
    #         date[key]=value
    #         re.pop('closed_on')
    #         logger.info("编号：" + str(re['id']) + "结束时间到date字典中.")
    #
    #     if 'done_ratio' in re.keys():
    #         key='完成率'
    #         value=re['done_ratio']
    #         date[key]=value
    #         re.pop('done_ratio')
    #
    #     if 'created_on' in re.keys():
    #         key = '创建日期'
    #         value = re['created_on']
    #         date[key] = value
    #         re.pop('created_on')
    #
    #     if 'updated_on' in re.keys():
    #         key = '更新于'
    #         value = re['updated_on']
    #         date[key] = value
    #         re.pop('updated_on')
    #
    #     re['date']=date


    if 'author' in re.keys():
        if re['author'] is not None:
            s=read(filename)
            d=re['author'].strip()
            t = len(d) + 1
            i = 0
            for i in range(len(s)):
                y=0
                if d in s[i]:
                    re['author']=s[i][t:]
                    y=1
                    logger.info("获取：" + str(re['author']) + "JIRA 登陆名.")
                    break
            if y==0:
                logger.info("获取：" + str(re['author']) + "JIRA 登陆名,失败")

    if 'assigned_to' in re.keys():
        if re['assigned_to'] is not None:

            s=read(filename)
            d=re['assigned_to'].strip()
            t = len(d) + 1
            i = 0

            for i in range(len(s)):
                y=0

                if d in s[i]:
                    re['assigned_to']=s[i][t:]
                    y=1
                    logger.info("获取：" + str(re['assigned_to']) + "JIRA 登陆名.")
                    break
            if y==0:
                logger.info("获取：" + str(re['assigned_to']) + "JIRA 登陆名,失败.")
    else:
        re['assigned_to']=re['author']

    if 'due_date' not in re.keys():
        re['due_date']=None

    if 'description' in re.keys():
        if re['description'] == None:
            re['description']=''

    if re['assigned_to']=='admin':
        re['assigned_to']='hongxiaomeng'

    if '测试周期' in re.keys():
        if re['测试周期']==None:
            re['测试周期']='系统测试-第一轮'

    if '测试环境' in re.keys():
        if re['测试环境']==None:
            re['测试环境']='测试环境'

    if '项目阶段' in re.keys():
        if re['项目阶段']==None:
            re['项目阶段']='上线前'
    return re

#更改任务状态
def transition(issue,issuekey):
    if 'status' in issue.keys():
        if issue['status'] is not None:
            if issue['tracker']=='缺陷' or issue['tracker']=='问题' or issue['tracker']=='错误' or issue['tracker']=='搁置':
                if issue['status']=='进行中':
                    jira.transition_issue(issuekey,'4')#更改状态至 进行中
                    logger.info(
                        "修改：" + issue['tracker']+str(issuekey) + "状态为“进行中”.##redmine标号：" + str(issue['id']))

                elif issue['status']=='已解决':
                    jira.transition_issue(issuekey,'5',resolution={'id': '1'})#更改状态至 已解决 ,解决结果 已修复
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“已解决”，解决结果 已修复.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '已关闭':
                    jira.transition_issue(issuekey, '5', resolution={'id': '1'})#更改状态至 已解决 ,解决结果 已修复
                    jira.transition_issue(issuekey, '781')#更改状态至 待验证 ,
                    jira.transition_issue(issuekey, '701')#更改状态至 已关闭
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“已关闭”，解决结果 已修复.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '已拒绝':
                    jira.transition_issue(issuekey, '711',resolution={'id': '2'})  # 更改状态至 已拒绝，解决结果 拒绝处理
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“已拒绝”，解决结果 拒绝处理.##redmine标号：" + str(issue['id']))


                elif issue['status'] == '回归未通过':
                    jira.transition_issue(issuekey, '5')#更改状态至 已解决
                    jira.transition_issue(issuekey, '781')#更改状态至 待验证 ,
                    jira.transition_issue(issuekey, '3')#更改状态至 重新打开
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“重新打开”.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '等待上预生产':
                    jira.transition_issue(issuekey,'5',resolution={'id': '1'})
                    jira.transition_issue(issuekey, '781')
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“待验证”.##redmine标号：" + str(issue['id']))

                else:
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“open”.##redmine标号：" + str(issue['id']))

            else:
                if issue['status'] == '已分派' or issue['status'] =='需求已确认':
                    jira.transition_issue(issuekey, '781')#更改状态至 已纳入开发计划 ,
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“已纳入开发计划”.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '进行中' or issue['status'] =='回归未通过':
                    jira.transition_issue(issuekey, '781')  # 更改状态至 已纳入开发计划
                    jira.transition_issue(issuekey, '4')#更改状态至 开发中
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“开发中”.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '已解决':
                    jira.transition_issue(issuekey, '781')  # 更改状态至 已纳入开发计划
                    jira.transition_issue(issuekey, '5')#更改状态至 开发完成
                    logger.info("修改：" + issue['tracker'] + str(issuekey) + "状态为“开发完成”.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '已拒绝':
                    jira.transition_issue(issuekey, '731', resolution={'id': '2'})  # 更改状态至 已拒绝，解决结果 拒绝处理
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“已拒绝”，解决结果 拒绝处理.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '已关闭':
                    jira.transition_issue(issuekey, '781')  # 更改状态至 已纳入开发计划
                    jira.transition_issue(issuekey, '5', resolution={'id': '1'})  # 更改状态至 开发完成，解决结果 已解决
                    jira.transition_issue(issuekey, '821')# 更改状态至 待验证
                    jira.transition_issue(issuekey, '701')# 更改状态至 测试通过
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“开发完成”，解决结果“已解决”.##redmine标号：" + str(issue['id']))

                elif issue['status'] == '等待上预生产':
                    jira.transition_issue(issuekey, '781')  # 更改状态至 已纳入开发计划
                    jira.transition_issue(issuekey, '5', resolution={'id': '1'})  # 更改状态至 开发完成，解决结果 已解决
                    jira.transition_issue(issuekey, '821')#更改状态至 待验证
                    logger.info(
                        "修改：" + issue['tracker'] + str(issuekey) + "状态为“待验证“，解决结果 ”已解决”.##redmine标号：" + str(issue['id']))
        else:
            logger.info("编号：" + str(issue['id']) + "无状态字段为 空.")
    else:
        logger.info("编号：" + str(issue['id']) + "无状态字段.")


#匹配jira字段
def issue_dict(Reissue):
    re=Reissue

    if re['tracker']=='缺陷':
        issuedict={
        'project': {'key': 'PFBP'},  # 项目
        'summary': str(re['id']) + re['subject'],  # 主题
        'description': re['description'],  # 描述
        'issuetype': {'name': re['tracker']},  # 问题类型
        'components': [{'name': re['业务模块']}],  # 模块
        'priority': {'name': re['priority']},  # 优先级
        'reporter': {'name':re['author']}, #报告人
        'assignee': {'name': re['assigned_to']},  # 经办人
        # 'assignee': {'name': 'hongxiaomeng'},  # 经办人
        'customfield_10611': {'value': re['测试周期']},  # 测试周期
        'customfield_10403': {'value': re['缺陷归因']},  # 缺陷归因
        'customfield_10203': {'value': re['测试环境']}, # 测试环境
        'customfield_10900':re['实际完成时间'],#实际完成时间
        'duedate':re['due_date']#到期日 or 计划完成日期
                   }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='功能':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '新需求'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            # 'customfield_10611': {'value': 'UAT'},  # 测试周期
            # 'customfield_10403': {'value': re['缺陷归因']},  # 缺陷归因
            # 'customfield_10203': {'value': re['测试环境']},  # 测试环境
            # 'customfield_10900':re['实际完成时间'],#实际完成时间

            'duedate':re['due_date']#到期日 or 计划完成日期
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='任务':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '任务'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            # 'customfield_10611': {'value': 'UAT'},  # 测试周期
            # 'customfield_10403': {'value': re['缺陷归因']},  # 缺陷归因
            # 'customfield_10203': {'value': re['测试环境']},  # 测试环境
            # 'customfield_10900':re['实际完成时间'],#实际完成时间
            'duedate':re['due_date']#到期日 or 计划完成日期
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='问题':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '缺陷'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            'customfield_10611': {'value': '用户体验测试'},  # 测试周期
            'customfield_10403': {'value': '其他'},  # 缺陷归因
            'customfield_10203': {'value': '测试环境'},  # 测试环境
            'customfield_10900':re['实际完成时间'],#实际完成时间
            'duedate':re['due_date']#到期日 or 计划完成日期
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='需求变更':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '需求变更'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            # 'customfield_10611': {'value': '用户体验测试'},  # 测试周期
            # 'customfield_10403': {'value': '其他'},  # 缺陷归因
            # 'customfield_10203': {'value': '测试环境'},  # 测试环境
            # 'customfield_10900':re['实际完成时间'],#实际完成时间
            # 'duedate':re['due_date']#到期日 or 计划完成日期
            'customfield_10902':re['需求计划完成时间'],
            'customfield_10903':re['需求实际完成时间'],
            'customfield_10904':re['开发计划完成时间'],
            'customfield_10905':re['开发实际完成时间'],
            'customfield_10907':re['UAT计划完成时间'],
            'customfield_10906':re['UAT实际完成时间'],
            'customfield_10908': re['需求确认计划耗时（人天）'],
            'customfield_10909': re['开发计划耗时（人天）'],
            'customfield_10910': re['UAT测试计划耗时（人天）'],
            'customfield_10901': {'value': re['项目阶段']} # 项目阶段
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='支持':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '任务'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            # 'customfield_10611': {'value': '用户体验测试'},  # 测试周期
            # 'customfield_10403': {'value': '其他'},  # 缺陷归因
            # 'customfield_10203': {'value': '测试环境'},  # 测试环境
            'duedate': re['due_date']  # 到期日 or 计划完成日期
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='搁置':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '缺陷'},  # 问题类型
            # 'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            'customfield_10611': {'value': '用户体验测试'},  # 测试周期
            'customfield_10403': {'value': '其他'},  # 缺陷归因
            'customfield_10203': {'value': '测试环境'},  # 测试环境
            'duedate': re['due_date']  # 到期日 or 计划完成日期
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker']=='错误':
        issuedict={
        'project': {'key': 'PFBP'},  # 项目
        'summary': str(re['id']) + re['subject'],  # 主题
        'description': re['description'],  # 描述
        'issuetype': {'name': '缺陷'},  # 问题类型
        # 'components': [{'name': re['业务模块']}],  # 模块
        'priority': {'name': re['priority']},  # 优先级
        'reporter': {'name': re['author']},  # 报告人
         'assignee': {'name': re['assigned_to']},  # 经办人
        'customfield_10611': {'value': re['测试周期']},  # 测试周期
        'customfield_10403': {'value': '其他'},  # 缺陷归因
        'customfield_10203': {'value': re['测试环境']}, # 测试环境
        'duedate': re['due_date']  # 到期日 or 计划完成日期
                   }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    elif re['tracker'] == '优化':
        issuedict = {
            'project': {'key': 'PFBP'},  # 项目
            'summary': str(re['id']) + re['subject'],  # 主题
            'description': re['description'],  # 描述
            'issuetype': {'name': '改进'},  # 问题类型
            'components': [{'name': re['业务模块']}],  # 模块
            'priority': {'name': re['priority']},  # 优先级
            'reporter': {'name': re['author']},  # 报告人
            'assignee': {'name': re['assigned_to']},  # 经办人
            # 'customfield_10611': {'value': re['测试周期']},  # 测试周期
            # 'customfield_10403': {'value': re['缺陷归因']},  # 缺陷归因
            # 'customfield_10203': {'value': re['测试环境']},  # 测试环境
            'customfield_10902': re['需求计划完成时间'],
            'customfield_10903': re['需求实际完成时间'],
            'customfield_10904': re['开发计划完成时间'],
            'customfield_10905': re['开发实际完成时间'],
            'customfield_10907': re['UAT计划完成时间'],
            'customfield_10906': re['UAT实际完成时间'],
            'customfield_10908': re['需求确认计划耗时（人天）'],
            'customfield_10909': re['开发计划耗时（人天）'],
            'customfield_10910': re['UAT测试计划耗时（人天）'],
            'customfield_10901': {'value': re['项目阶段']}
        }
        logger.info("创建jira：" + issue['tracker'] + ".##redmine标号：" + str(issue['id']))
        return issuedict

    # elif re['tracker'] == 'sql部署':
    #     logger.info("编号为："+str(id)+"的任务属于sql部署，不做考虑")

    else:
        logger.info("编号为：" + str(id) + "的任务无对应任务类型")
        return None

def read(textname):
    with open(textname, 'r',encoding='utf-8') as f:
        lines = f.read().splitlines()
        return lines

def write(textname,line):
    with open(textname,'a') as f:
        # print(str(line1)+"$$$$$$$$$$$$$$$")
        f.write(str(line)+'\n')

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('simpleExample')

    id_file='nname.txt'
    author_file="author_file.txt"

    jira = JIRA('http://172.30.0.108:8080/', basic_auth=('hongxiaomeng', 'hong123'))
    sql_count=0
    for id in range(1011,1012):
        if str(id) not in read(id_file):
            try:
                r=redmine(id)
            except:
                logger.info("无编号为："+str(id)+"的任务")
            else:
                re_issue = dictget(r['issue'])
                if re_issue['tracker'] == 'sql部署':
                    sql_count+=1
                    jira_issue=None
                    logger.info("编号为：" + str(id) + "的任务属于sql部署，不做考虑")
                else:
                    logger.debug(re_issue)
                    issue=change(re_issue,author_file)
                    logger.debug(issue)
                    jira_issue=issue_dict(issue)
                    logger.debug(jira_issue)

                if jira_issue is not None:
                    new_issue = jira.create_issue(fields=jira_issue)

                    issuekey = new_issue.key

                    transition(issue,issuekey)


                    if '备注' in issue.keys():
                        add_comment(issuekey, issue)
                    else:
                        print("编号为：" + str(id) + "的任务,无备注")

                    add_attachment(issuekey, issue)

                    write(id_file,id)

        else:
            print("编号为："+str(id)+"已创建")

    logger.info("类型为sql的任务总数为："+str(sql_count))
