from qtpp.libs.framework import libs
from qtpp.libs.framework.responseResult import (
    OutPutParam, 
    Check_Result
)
from qtpp.libs.framework.asserts import BY_HOW, BY_T


class EXTS:
  @staticmethod
  def get_out_parameters(params_list):
      '''
      整理出参参数
      '''
      
      # 出参内容
      ret_param = []

      # 出参不为空
      if params_list['data']:

        for param in params_list:
          ret_param.append(
            OutPutParam.get_output_variable_value(
              param['source'],
              param['name'],
              response,
              param['exp'],
              param['match']
            )
          )
      return ret_param

  @staticmethod
  def debug_or_save(req, out_param, response, odb):
    # debug and save保存到数据库
    if req['debugWay']  == 1:
      for i, val in enumerate(req['assert']['data']):
          refer = out_param[val['checkObject']]['var_value'] if val['checkType'] == BY_T.REFER else ''
          chk_result = Check_Result.get_check_result(
              response=response,
              checkType=val['checkType'],
              check_object=val['checkObject'],
              chk_cd=val['checkCondition'],
              check_content=val['checkContent'],
              REFER=refer
          )
          case_assert = Case_Assert(
              c_id=req['caseId'],
              check_type=val['checkType'],
              check_object=chk_result['check_object'],
              check_condition=val['checkCondition'],
              check_content=chk_result['check_content'],
              check_result=chk_result['check_result']
          )
          # assert结果写入，断言表
          odb.add(case_assert)
          case_result = Case_Result(
              c_id=req['caseId'],
              response_header= repr(response.headers),
              response_body=response.text,
              response_cookies=repr(libs.dict_from_cookiejar(
                  response.cookies
              )),
              response_datatime=int(response.elapsed.total_seconds() * 1000)
          )
          # assert响应结果写入，结果表
          odb.add(case_result)