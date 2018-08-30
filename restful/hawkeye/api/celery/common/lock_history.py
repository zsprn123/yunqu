# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/common/lock_history.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9228 bytes
Instruction context:
   
 109     858  LOAD_GLOBAL              'logger'
            860  LOAD_ATTR                'error'
            862  LOAD_GLOBAL              'str'
            864  LOAD_FAST                'e'
            866  CALL_FUNCTION_1       1  ''
            868  CALL_FUNCTION_1       1  ''
            870  POP_TOP          
            872  POP_BLOCK        
            874  POP_EXCEPT       
            876  LOAD_CONST               None
          878_0  COME_FROM_FINALLY   856  '856'
            878  LOAD_CONST               None
            880  STORE_FAST               'e'
            882  DELETE_FAST              'e'
            884  END_FINALLY      
            886  JUMP_FORWARD        890  'to 890'
            888  END_FINALLY      
          890_0  COME_FROM           886  '886'
          890_1  COME_FROM           838  '838'
            890  JUMP_BACK           586  'to 586'
            894  POP_BLOCK        
->          896  JUMP_FORWARD       1204  'to 1204'
            900  ELSE                     '1204'
from alarm.enum.alarm_warn_enum import WARN_ENUM
from api.v1.alarm.services.warnService import customized_warn_scanner
from monitor.models import MySQL_Lock_History, Oracle_Lock_History, DB2_Lock_History, MSSQL_Lock_History, Transaction, Performance
from api.v1.monitor.services.runsqlService import run_batch_sql
from api.enum.lock_history_enum import get_blocking_session_detail, save_session_detail_list
from common.util import build_exception_from_java
from datetime import datetime
from api.enum.lock_history_enum import get_lock_query
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

def save_lock_history--- This code section failed: ---

  18       0  LOAD_FAST                'database'
           2  LOAD_ATTR                'db_type'
           4  STORE_FAST               'db_type'

  19       6  LOAD_FAST                'db_type'
           8  LOAD_CONST               'oracle'
          10  COMPARE_OP               '=='
          12  POP_JUMP_IF_FALSE   312  'to 312'

  20      16  SETUP_LOOP         1204  'to 1204'
          20  LOAD_FAST                'lock_list'
          22  GET_ITER         
          24  FOR_ITER            306  'to 306'
          28  STORE_FAST               'x'

  21      30  LOAD_GLOBAL              'Oracle_Lock_History'
          32  CALL_FUNCTION_0       0  ''
          34  STORE_FAST               'lock'

  22      36  LOAD_FAST                'x'
          38  LOAD_ATTR                'get'
          40  LOAD_CONST               'B_RES'
          42  CALL_FUNCTION_1       1  ''
          44  LOAD_FAST                'lock'
          46  STORE_ATTR               'b_res'

  23      48  LOAD_FAST                'x'
          50  LOAD_ATTR                'get'
          52  LOAD_CONST               'B_BLOCKER'
          54  CALL_FUNCTION_1       1  ''
          56  LOAD_FAST                'lock'
          58  STORE_ATTR               'b_blocker'

  24      60  LOAD_FAST                'x'
          62  LOAD_ATTR                'get'
          64  LOAD_CONST               'B_BLOCKED_CNT'
          66  CALL_FUNCTION_1       1  ''
          68  LOAD_FAST                'lock'
          70  STORE_ATTR               'b_blocked_cnt'

  25      72  LOAD_FAST                'x'
          74  LOAD_ATTR                'get'
          76  LOAD_CONST               'B_REQUEST'
          78  CALL_FUNCTION_1       1  ''
          80  LOAD_FAST                'lock'
          82  STORE_ATTR               'b_request'

  26      84  LOAD_FAST                'x'
          86  LOAD_ATTR                'get'
          88  LOAD_CONST               'B_LMODE'
          90  CALL_FUNCTION_1       1  ''
          92  LOAD_FAST                'lock'
          94  STORE_ATTR               'b_lmode'

  27      96  LOAD_FAST                'x'
          98  LOAD_ATTR                'get'
         100  LOAD_CONST               'B_USERNAME'
         102  CALL_FUNCTION_1       1  ''
         104  LOAD_FAST                'lock'
         106  STORE_ATTR               'b_username'

  28     108  LOAD_FAST                'x'
         110  LOAD_ATTR                'get'
         112  LOAD_CONST               'B_SQL_ID'
         114  CALL_FUNCTION_1       1  ''
         116  LOAD_FAST                'lock'
         118  STORE_ATTR               'b_sql_id'

  30     120  LOAD_FAST                'x'
         122  LOAD_ATTR                'get'
         124  LOAD_CONST               'B_PREV_SQL_ID'
         126  CALL_FUNCTION_1       1  ''
         128  LOAD_FAST                'lock'
         130  STORE_ATTR               'b_prev_sql_id'

  32     132  LOAD_FAST                'x'
         134  LOAD_ATTR                'get'
         136  LOAD_CONST               'B_CTIME'
         138  CALL_FUNCTION_1       1  ''
         140  LOAD_FAST                'lock'
         142  STORE_ATTR               'b_ctime'

  33     144  LOAD_FAST                'x'
         146  LOAD_ATTR                'get'
         148  LOAD_CONST               'W_WAITER'
         150  CALL_FUNCTION_1       1  ''
         152  LOAD_FAST                'lock'
         154  STORE_ATTR               'w_waiter'

  34     156  LOAD_FAST                'x'
         158  LOAD_ATTR                'get'
         160  LOAD_CONST               'W_REQUEST'
         162  CALL_FUNCTION_1       1  ''
         164  LOAD_FAST                'lock'
         166  STORE_ATTR               'w_request'

  35     168  LOAD_FAST                'x'
         170  LOAD_ATTR                'get'
         172  LOAD_CONST               'W_LMODE'
         174  CALL_FUNCTION_1       1  ''
         176  LOAD_FAST                'lock'
         178  STORE_ATTR               'w_lmode'

  36     180  LOAD_FAST                'x'
         182  LOAD_ATTR                'get'
         184  LOAD_CONST               'W_USERNAME'
         186  CALL_FUNCTION_1       1  ''
         188  LOAD_FAST                'lock'
         190  STORE_ATTR               'w_username'

  37     192  LOAD_FAST                'x'
         194  LOAD_ATTR                'get'
         196  LOAD_CONST               'W_SQL_ID'
         198  CALL_FUNCTION_1       1  ''
         200  LOAD_FAST                'lock'
         202  STORE_ATTR               'w_sql_id'

  39     204  LOAD_FAST                'x'
         206  LOAD_ATTR                'get'
         208  LOAD_CONST               'W_PREV_SQL_ID'
         210  CALL_FUNCTION_1       1  ''
         212  LOAD_FAST                'lock'
         214  STORE_ATTR               'w_prev_sql_id'

  41     216  LOAD_FAST                'x'
         218  LOAD_ATTR                'get'
         220  LOAD_CONST               'W_CTIME'
         222  CALL_FUNCTION_1       1  ''
         224  LOAD_FAST                'lock'
         226  STORE_ATTR               'w_ctime'

  43     228  LOAD_FAST                'created_at'
         230  LOAD_FAST                'lock'
         232  STORE_ATTR               'created_at'

  45     234  LOAD_FAST                'database'
         236  LOAD_FAST                'lock'
         238  STORE_ATTR               'database'

  47     240  SETUP_EXCEPT        254  'to 254'

  48     242  LOAD_FAST                'lock'
         244  LOAD_ATTR                'save'
         246  CALL_FUNCTION_0       0  ''
         248  POP_TOP          
         250  POP_BLOCK        
         252  JUMP_BACK            24  'to 24'
       254_0  COME_FROM_EXCEPT    240  '240'

  49     254  DUP_TOP          
         256  LOAD_GLOBAL              'Exception'
         258  COMPARE_OP               'exception-match'
         260  POP_JUMP_IF_FALSE   302  'to 302'
         264  POP_TOP          
         266  STORE_FAST               'e'
         268  POP_TOP          
         270  SETUP_FINALLY       292  'to 292'

  50     272  LOAD_GLOBAL              'logger'
         274  LOAD_ATTR                'error'
         276  LOAD_GLOBAL              'str'
         278  LOAD_FAST                'e'
         280  CALL_FUNCTION_1       1  ''
         282  CALL_FUNCTION_1       1  ''
         284  POP_TOP          
         286  POP_BLOCK        
         288  POP_EXCEPT       
         290  LOAD_CONST               None
       292_0  COME_FROM_FINALLY   270  '270'
         292  LOAD_CONST               None
         294  STORE_FAST               'e'
         296  DELETE_FAST              'e'
         298  END_FINALLY      
         300  JUMP_BACK            24  'to 24'
         302  END_FINALLY      
         304  JUMP_BACK            24  'to 24'
         306  POP_BLOCK        
       308_0  COME_FROM_LOOP       16  '16'
         308  JUMP_FORWARD       1204  'to 1204'
         312  ELSE                     '1204'

  52     312  LOAD_FAST                'db_type'
         314  LOAD_CONST               'mysql'
         316  COMPARE_OP               '=='
         318  POP_JUMP_IF_FALSE   568  'to 568'

  53     322  SETUP_LOOP          564  'to 564'
         324  LOAD_FAST                'lock_list'
         326  GET_ITER         
         328  FOR_ITER            562  'to 562'
         330  STORE_FAST               'x'

  54     332  LOAD_GLOBAL              'MySQL_Lock_History'
         334  CALL_FUNCTION_0       0  ''
         336  STORE_FAST               'lock'

  56     338  LOAD_FAST                'x'
         340  LOAD_ATTR                'get'
         342  LOAD_CONST               'B_RES'
         344  CALL_FUNCTION_1       1  ''
         346  LOAD_FAST                'lock'
         348  STORE_ATTR               'b_res'

  57     350  LOAD_FAST                'x'
         352  LOAD_ATTR                'get'
         354  LOAD_CONST               'W_TRX_ID'
         356  CALL_FUNCTION_1       1  ''
         358  LOAD_FAST                'lock'
         360  STORE_ATTR               'w_trx_id'

  58     362  LOAD_FAST                'x'
         364  LOAD_ATTR                'get'
         366  LOAD_CONST               'W_WAITER'
         368  CALL_FUNCTION_1       1  ''
         370  LOAD_FAST                'lock'
         372  STORE_ATTR               'w_waiter'

  59     374  LOAD_FAST                'x'
         376  LOAD_ATTR                'get'
         378  LOAD_CONST               'W_WAIT_TIME'
         380  CALL_FUNCTION_1       1  ''
         382  LOAD_FAST                'lock'
         384  STORE_ATTR               'w_wait_time'

  60     386  LOAD_FAST                'x'
         388  LOAD_ATTR                'get'
         390  LOAD_CONST               'W_WAITING_QUERY'
         392  CALL_FUNCTION_1       1  ''
         394  LOAD_FAST                'lock'
         396  STORE_ATTR               'w_waiting_query'

  61     398  LOAD_FAST                'x'
         400  LOAD_ATTR                'get'
         402  LOAD_CONST               'W_WAITING_TABLE_LOCK'
         404  CALL_FUNCTION_1       1  ''
         406  LOAD_FAST                'lock'
         408  STORE_ATTR               'w_waiting_table_lock'

  62     410  LOAD_FAST                'x'
         412  LOAD_ATTR                'get'
         414  LOAD_CONST               'B_TRX_ID'
         416  CALL_FUNCTION_1       1  ''
         418  LOAD_FAST                'lock'
         420  STORE_ATTR               'b_trx_id'

  63     422  LOAD_FAST                'x'
         424  LOAD_ATTR                'get'
         426  LOAD_CONST               'B_BLOCKER'
         428  CALL_FUNCTION_1       1  ''
         430  LOAD_FAST                'lock'
         432  STORE_ATTR               'b_blocker'

  64     434  LOAD_FAST                'x'
         436  LOAD_ATTR                'get'
         438  LOAD_CONST               'B_HOST'
         440  CALL_FUNCTION_1       1  ''
         442  LOAD_FAST                'lock'
         444  STORE_ATTR               'b_host'

  65     446  LOAD_FAST                'x'
         448  LOAD_ATTR                'get'
         450  LOAD_CONST               'B_PORT'
         452  CALL_FUNCTION_1       1  ''
         454  LOAD_FAST                'lock'
         456  STORE_ATTR               'b_port'

  66     458  LOAD_FAST                'x'
         460  LOAD_ATTR                'get'
         462  LOAD_CONST               'B_IDLE_IN_TRX'
         464  CALL_FUNCTION_1       1  ''
         466  LOAD_FAST                'lock'
         468  STORE_ATTR               'b_idle_in_trx'

  67     470  LOAD_FAST                'x'
         472  LOAD_ATTR                'get'
         474  LOAD_CONST               'B_TRX_QUERY'
         476  CALL_FUNCTION_1       1  ''
         478  LOAD_FAST                'lock'
         480  STORE_ATTR               'b_trx_query'

  69     482  LOAD_FAST                'created_at'
         484  LOAD_FAST                'lock'
         486  STORE_ATTR               'created_at'

  70     488  LOAD_FAST                'database'
         490  LOAD_FAST                'lock'
         492  STORE_ATTR               'database'

  72     494  SETUP_EXCEPT        508  'to 508'

  73     496  LOAD_FAST                'lock'
         498  LOAD_ATTR                'save'
         500  CALL_FUNCTION_0       0  ''
         502  POP_TOP          
         504  POP_BLOCK        
         506  JUMP_FORWARD        558  'to 558'
       508_0  COME_FROM_EXCEPT    494  '494'

  74     508  DUP_TOP          
         510  LOAD_GLOBAL              'Exception'
         512  COMPARE_OP               'exception-match'
         514  POP_JUMP_IF_FALSE   556  'to 556'
         518  POP_TOP          
         520  STORE_FAST               'e'
         522  POP_TOP          
         524  SETUP_FINALLY       546  'to 546'

  75     526  LOAD_GLOBAL              'logger'
         528  LOAD_ATTR                'error'
         530  LOAD_GLOBAL              'str'
         532  LOAD_FAST                'e'
         534  CALL_FUNCTION_1       1  ''
         536  CALL_FUNCTION_1       1  ''
         538  POP_TOP          
         540  POP_BLOCK        
         542  POP_EXCEPT       
         544  LOAD_CONST               None
       546_0  COME_FROM_FINALLY   524  '524'
         546  LOAD_CONST               None
         548  STORE_FAST               'e'
         550  DELETE_FAST              'e'
         552  END_FINALLY      
         554  JUMP_FORWARD        558  'to 558'
         556  END_FINALLY      
       558_0  COME_FROM           554  '554'
       558_1  COME_FROM           506  '506'
         558  JUMP_BACK           328  'to 328'
         562  POP_BLOCK        
       564_0  COME_FROM_LOOP      322  '322'
         564  JUMP_FORWARD       1204  'to 1204'
         568  ELSE                     '1204'

  77     568  LOAD_FAST                'db_type'
         570  LOAD_CONST               'db2'
         572  COMPARE_OP               '=='
         574  POP_JUMP_IF_FALSE   900  'to 900'

  78     578  SETUP_LOOP         1204  'to 1204'
         582  LOAD_FAST                'lock_list'
         584  GET_ITER         
         586  FOR_ITER            894  'to 894'
         590  STORE_FAST               'x'

  79     592  LOAD_GLOBAL              'DB2_Lock_History'
         594  CALL_FUNCTION_0       0  ''
         596  STORE_FAST               'lock'

  80     598  LOAD_FAST                'x'
         600  LOAD_ATTR                'get'
         602  LOAD_CONST               'B_RES'
         604  CALL_FUNCTION_1       1  ''
         606  LOAD_FAST                'lock'
         608  STORE_ATTR               'b_res'

  81     610  LOAD_FAST                'x'
         612  LOAD_ATTR                'get'
         614  LOAD_CONST               'LOCK_OBJECT_TYPE'
         616  CALL_FUNCTION_1       1  ''
         618  LOAD_FAST                'lock'
         620  STORE_ATTR               'lock_object_type'

  82     622  LOAD_FAST                'x'
         624  LOAD_ATTR                'get'
         626  LOAD_CONST               'LOCK_WAIT_ELAPSED_TIME'
         628  CALL_FUNCTION_1       1  ''
         630  LOAD_FAST                'lock'
         632  STORE_ATTR               'lock_wait_elapsed_time'

  83     634  LOAD_FAST                'x'
         636  LOAD_ATTR                'get'
         638  LOAD_CONST               'OWNER'
         640  CALL_FUNCTION_1       1  ''
         642  LOAD_FAST                'lock'
         644  STORE_ATTR               'tabschema'

  84     646  LOAD_FAST                'x'
         648  LOAD_ATTR                'get'
         650  LOAD_CONST               'TABLE_NAME'
         652  CALL_FUNCTION_1       1  ''
         654  LOAD_FAST                'lock'
         656  STORE_ATTR               'tabname'

  87     658  LOAD_FAST                'x'
         660  LOAD_ATTR                'get'
         662  LOAD_CONST               'LOCK_CURRENT_MODE'
         664  CALL_FUNCTION_1       1  ''
         666  LOAD_FAST                'lock'
         668  STORE_ATTR               'lock_current_mode'

  88     670  LOAD_FAST                'x'
         672  LOAD_ATTR                'get'
         674  LOAD_CONST               'LOCK_MODE_REQUESTED'
         676  CALL_FUNCTION_1       1  ''
         678  LOAD_FAST                'lock'
         680  STORE_ATTR               'lock_mode_requested'

  89     682  LOAD_FAST                'x'
         684  LOAD_ATTR                'get'
         686  LOAD_CONST               'W_WAITER'
         688  CALL_FUNCTION_1       1  ''
         690  LOAD_FAST                'lock'
         692  STORE_ATTR               'w_waiter'

  90     694  LOAD_FAST                'x'
         696  LOAD_ATTR                'get'
         698  LOAD_CONST               'REQ_AGENT_TID'
         700  CALL_FUNCTION_1       1  ''
         702  LOAD_FAST                'lock'
         704  STORE_ATTR               'req_agent_tid'

  92     706  LOAD_FAST                'x'
         708  LOAD_ATTR                'get'
         710  LOAD_CONST               'REQ_APPLICATION_NAME'
         712  CALL_FUNCTION_1       1  ''
         714  LOAD_FAST                'lock'
         716  STORE_ATTR               'req_application_name'

  93     718  LOAD_FAST                'x'
         720  LOAD_ATTR                'get'
         722  LOAD_CONST               'REQ_USERID'
         724  CALL_FUNCTION_1       1  ''
         726  LOAD_FAST                'lock'
         728  STORE_ATTR               'req_userid'

  94     730  LOAD_FAST                'x'
         732  LOAD_ATTR                'get'
         734  LOAD_CONST               'REQ_EXECUTABLE_ID'
         736  CALL_FUNCTION_1       1  ''
         738  LOAD_FAST                'lock'
         740  STORE_ATTR               'req_executable_id'

  95     742  LOAD_FAST                'x'
         744  LOAD_ATTR                'get'
         746  LOAD_CONST               'REQ_STMT_TEXT'
         748  CALL_FUNCTION_1       1  ''
         750  LOAD_FAST                'lock'
         752  STORE_ATTR               'req_stmt_text'

  96     754  LOAD_FAST                'x'
         756  LOAD_ATTR                'get'
         758  LOAD_CONST               'B_BLOCKER'
         760  CALL_FUNCTION_1       1  ''
         762  LOAD_FAST                'lock'
         764  STORE_ATTR               'b_blocker'

  98     766  LOAD_FAST                'x'
         768  LOAD_ATTR                'get'
         770  LOAD_CONST               'HLD_APPLICATION_NAME'
         772  CALL_FUNCTION_1       1  ''
         774  LOAD_FAST                'lock'
         776  STORE_ATTR               'hld_application_name'

  99     778  LOAD_FAST                'x'
         780  LOAD_ATTR                'get'
         782  LOAD_CONST               'HLD_USERID'
         784  CALL_FUNCTION_1       1  ''
         786  LOAD_FAST                'lock'
         788  STORE_ATTR               'hld_userid'

 100     790  LOAD_FAST                'x'
         792  LOAD_ATTR                'get'
         794  LOAD_CONST               'HLD_CURRENT_STMT_TEXT'
         796  CALL_FUNCTION_1       1  ''
         798  LOAD_FAST                'lock'
         800  STORE_ATTR               'hld_current_stmt_text'

 101     802  LOAD_FAST                'x'
         804  LOAD_ATTR                'get'
         806  LOAD_CONST               'HLD_EXECUTABLE_ID'
         808  CALL_FUNCTION_1       1  ''
         810  LOAD_FAST                'lock'
         812  STORE_ATTR               'hld_executable_id'

 103     814  LOAD_FAST                'created_at'
         816  LOAD_FAST                'lock'
         818  STORE_ATTR               'created_at'

 104     820  LOAD_FAST                'database'
         822  LOAD_FAST                'lock'
         824  STORE_ATTR               'database'

 106     826  SETUP_EXCEPT        840  'to 840'

 107     828  LOAD_FAST                'lock'
         830  LOAD_ATTR                'save'
         832  CALL_FUNCTION_0       0  ''
         834  POP_TOP          
         836  POP_BLOCK        
         838  JUMP_FORWARD        890  'to 890'
       840_0  COME_FROM_EXCEPT    826  '826'

 108     840  DUP_TOP          
         842  LOAD_GLOBAL              'Exception'
         844  COMPARE_OP               'exception-match'
         846  POP_JUMP_IF_FALSE   888  'to 888'
         850  POP_TOP          
         852  STORE_FAST               'e'
         854  POP_TOP          
         856  SETUP_FINALLY       878  'to 878'

 109     858  LOAD_GLOBAL              'logger'
         860  LOAD_ATTR                'error'
         862  LOAD_GLOBAL              'str'
         864  LOAD_FAST                'e'
         866  CALL_FUNCTION_1       1  ''
         868  CALL_FUNCTION_1       1  ''
         870  POP_TOP          
         872  POP_BLOCK        
         874  POP_EXCEPT       
         876  LOAD_CONST               None
       878_0  COME_FROM_FINALLY   856  '856'
         878  LOAD_CONST               None
         880  STORE_FAST               'e'
         882  DELETE_FAST              'e'
         884  END_FINALLY      
         886  JUMP_FORWARD        890  'to 890'
         888  END_FINALLY      
       890_0  COME_FROM           886  '886'
       890_1  COME_FROM           838  '838'
         890  JUMP_BACK           586  'to 586'
         894  POP_BLOCK        
         896  JUMP_FORWARD       1204  'to 1204'
         900  ELSE                     '1204'

 111     900  LOAD_FAST                'db_type'
         902  LOAD_CONST               'sqlserver'
         904  COMPARE_OP               '=='
         906  POP_JUMP_IF_FALSE  1204  'to 1204'

 112     910  SETUP_LOOP         1204  'to 1204'
         914  LOAD_FAST                'lock_list'
         916  GET_ITER         
         918  FOR_ITER           1202  'to 1202'
         922  STORE_FAST               'x'

 113     924  LOAD_GLOBAL              'MSSQL_Lock_History'
         926  CALL_FUNCTION_0       0  ''
         928  STORE_FAST               'lock'

 115     930  LOAD_FAST                'x'
         932  LOAD_ATTR                'get'
         934  LOAD_CONST               'B_BLOCKER'
         936  CALL_FUNCTION_1       1  ''
         938  LOAD_FAST                'lock'
         940  STORE_ATTR               'b_blocker'

 116     942  LOAD_FAST                'x'
         944  LOAD_ATTR                'get'
         946  LOAD_CONST               'B_LOGIN_NAME'
         948  CALL_FUNCTION_1       1  ''
         950  LOAD_FAST                'lock'
         952  STORE_ATTR               'b_login_name'

 117     954  LOAD_FAST                'x'
         956  LOAD_ATTR                'get'
         958  LOAD_CONST               'B_STATUS'
         960  CALL_FUNCTION_1       1  ''
         962  LOAD_FAST                'lock'
         964  STORE_ATTR               'b_status'

 118     966  LOAD_FAST                'x'
         968  LOAD_ATTR                'get'
         970  LOAD_CONST               'B_TEXT'
         972  CALL_FUNCTION_1       1  ''
         974  LOAD_FAST                'lock'
         976  STORE_ATTR               'b_text'

 119     978  LOAD_FAST                'x'
         980  LOAD_ATTR                'get'
         982  LOAD_CONST               'B_SQL_HANDLE'
         984  CALL_FUNCTION_1       1  ''
         986  LOAD_FAST                'lock'
         988  STORE_ATTR               'b_sql_handle'

 120     990  LOAD_FAST                'x'
         992  LOAD_ATTR                'get'
         994  LOAD_CONST               'W_WAITER'
         996  CALL_FUNCTION_1       1  ''
         998  LOAD_FAST                'lock'
        1000  STORE_ATTR               'w_waiter'

 121    1002  LOAD_FAST                'x'
        1004  LOAD_ATTR                'get'
        1006  LOAD_CONST               'W_LOGIN_NAME'
        1008  CALL_FUNCTION_1       1  ''
        1010  LOAD_FAST                'lock'
        1012  STORE_ATTR               'w_login_name'

 122    1014  LOAD_FAST                'x'
        1016  LOAD_ATTR                'get'
        1018  LOAD_CONST               'W_STATUS'
        1020  CALL_FUNCTION_1       1  ''
        1022  LOAD_FAST                'lock'
        1024  STORE_ATTR               'w_status'

 123    1026  LOAD_FAST                'x'
        1028  LOAD_ATTR                'get'
        1030  LOAD_CONST               'W_WAITDURATION'
        1032  CALL_FUNCTION_1       1  ''
        1034  LOAD_FAST                'lock'
        1036  STORE_ATTR               'w_waitduration'

 124    1038  LOAD_FAST                'x'
        1040  LOAD_ATTR                'get'
        1042  LOAD_CONST               'W_WAITTYPE'
        1044  CALL_FUNCTION_1       1  ''
        1046  LOAD_FAST                'lock'
        1048  STORE_ATTR               'w_waittype'

 125    1050  LOAD_FAST                'x'
        1052  LOAD_ATTR                'get'
        1054  LOAD_CONST               'W_WAITREQUESTMODE'
        1056  CALL_FUNCTION_1       1  ''
        1058  LOAD_FAST                'lock'
        1060  STORE_ATTR               'w_waitrequestmode'

 126    1062  LOAD_FAST                'x'
        1064  LOAD_ATTR                'get'
        1066  LOAD_CONST               'B_RES'
        1068  CALL_FUNCTION_1       1  ''
        1070  LOAD_FAST                'lock'
        1072  STORE_ATTR               'b_res'

 127    1074  LOAD_FAST                'x'
        1076  LOAD_ATTR                'get'
        1078  LOAD_CONST               'W_WAITRESOURCETYPE'
        1080  CALL_FUNCTION_1       1  ''
        1082  LOAD_FAST                'lock'
        1084  STORE_ATTR               'w_waitresourcetype'

 128    1086  LOAD_FAST                'x'
        1088  LOAD_ATTR                'get'
        1090  LOAD_CONST               'W_WAITRESOURCEDATABASENAME'
        1092  CALL_FUNCTION_1       1  ''
        1094  LOAD_FAST                'lock'
        1096  STORE_ATTR               'w_waitresourcedatabasename'

 129    1098  LOAD_FAST                'x'
        1100  LOAD_ATTR                'get'
        1102  LOAD_CONST               'W_TEXT'
        1104  CALL_FUNCTION_1       1  ''
        1106  LOAD_FAST                'lock'
        1108  STORE_ATTR               'w_text'

 130    1110  LOAD_FAST                'x'
        1112  LOAD_ATTR                'get'
        1114  LOAD_CONST               'W_SQL_HANDLE'
        1116  CALL_FUNCTION_1       1  ''
        1118  LOAD_FAST                'lock'
        1120  STORE_ATTR               'w_sql_handle'

 132    1122  LOAD_FAST                'created_at'
        1124  LOAD_FAST                'lock'
        1126  STORE_ATTR               'created_at'

 133    1128  LOAD_FAST                'database'
        1130  LOAD_FAST                'lock'
        1132  STORE_ATTR               'database'

 135    1134  SETUP_EXCEPT       1148  'to 1148'

 136    1136  LOAD_FAST                'lock'
        1138  LOAD_ATTR                'save'
        1140  CALL_FUNCTION_0       0  ''
        1142  POP_TOP          
        1144  POP_BLOCK        
        1146  JUMP_FORWARD       1198  'to 1198'
      1148_0  COME_FROM_EXCEPT   1134  '1134'

 137    1148  DUP_TOP          
        1150  LOAD_GLOBAL              'Exception'
        1152  COMPARE_OP               'exception-match'
        1154  POP_JUMP_IF_FALSE  1196  'to 1196'
        1158  POP_TOP          
        1160  STORE_FAST               'e'
        1162  POP_TOP          
        1164  SETUP_FINALLY      1186  'to 1186'

 138    1166  LOAD_GLOBAL              'logger'
        1168  LOAD_ATTR                'error'
        1170  LOAD_GLOBAL              'str'
        1172  LOAD_FAST                'e'
        1174  CALL_FUNCTION_1       1  ''
        1176  CALL_FUNCTION_1       1  ''
        1178  POP_TOP          
        1180  POP_BLOCK        
        1182  POP_EXCEPT       
        1184  LOAD_CONST               None
      1186_0  COME_FROM_FINALLY  1164  '1164'
        1186  LOAD_CONST               None
        1188  STORE_FAST               'e'
        1190  DELETE_FAST              'e'
        1192  END_FINALLY      
        1194  JUMP_FORWARD       1198  'to 1198'
        1196  END_FINALLY      
      1198_0  COME_FROM          1194  '1194'
      1198_1  COME_FROM          1146  '1146'
        1198  JUMP_BACK           918  'to 918'
        1202  POP_BLOCK        
      1204_0  COME_FROM_LOOP      910  '910'
      1204_1  COME_FROM           906  '906'
      1204_2  COME_FROM           896  '896'
      1204_3  COME_FROM           564  '564'
      1204_4  COME_FROM           308  '308'

Parse error at or near `JUMP_FORWARD' instruction at offset 896


def lock_history(database):
    query = get_lock_query(database)
    flag, json_data = run_batch_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return
    created_at = datetime.now.replace(microsecond=0)
    session_list = []
    if json_data.get('lock'):
        session_list = get_blocking_session_detail(database)
    lock_list = json_data.get('lock') if json_data.get('lock') else []
    save_lock_history(database, lock_list, created_at)
    transactions = json_data.get('transaction')
    trans = Transaction
    trans.database = database
    trans.created_at = created_at
    trans.transactions = transactions
    trans.save
    db_type = database.db_type
    locks = len(json_data.get('lock')) if json_data.get('lock') else 0
    warn = WARN_ENUM.get(db_type).Blocking_Session_Warn
    p = Performance(inst_id=database.db_name, name=warn.name, value=locks, created_at=created_at)
    customized_warn_scanner(warn, p, database, False)
    if transactions:
        warn = WARN_ENUM.get(db_type).Long_Transaction_Warn
        p = Performance(inst_id=database.db_name, name=warn.name, created_at=created_at)
        for t in transactions:
            options = {'SESSION_ID':t.get('SESSION_ID'),  'MACHINE':t.get('MACHINE'), 
             'TRX_STARTED':t.get('TRX_STARTED')}
            if t.get('INST_ID'):
                p.inst_id = t.get('INST_ID')
            p.value = t.get('TRX_SECONDS')
            if customized_warn_scanner(warn, p, database, False, options, True):
                session_list.append(t.get('SESSION_ID'))

        warn = WARN_ENUM.get(db_type).Transaction_Warn
        p = Performance(inst_id=database.db_name, name=warn.name, value=len(transactions), created_at=created_at)
        customized_warn_scanner(warn, p, database, False, {}, True)
        warn = WARN_ENUM.get(db_type).Big_Transaction_Warn
        p = Performance(inst_id=database.db_name, name=warn.name, created_at=created_at)
        big_transaction_key_dict = {'oracle':'USED_UBLK', 
         'mysql':'TRX_ROWS_MODIFIED', 
         'db2':'UOW_LOG_SPACE_USED', 
         'sqlserver':'LOG_BYTES'}
        for x in transactions:
            options = {'session_id':x.get('SESSION_ID'), 
             'start_time':x.get('TRX_STARTED')}
            if t.get('INST_ID'):
                p.inst_id = t.get('INST_ID')
            p.value = x.get(big_transaction_key_dict.get(db_type))
            if customized_warn_scanner(warn, p, database, False, options, True):
                session_list.append(t.get('SESSION_ID'))

    save_session_detail_list(database, list(set(session_list)))
    if db_type == 'mysql':
        lock_tables = json_data.get('tables')
        if lock_tables:
            if len(lock_tables):
                warn = WARN_ENUM.get(database.db_type).Locked_Table_Warn
                p = Performance(inst_id=database.db_name, name=warn.name, value=len(lock_tables), created_at=created_at)
                table_list = [('{}.{}').format(x.get('Database'), x.get('Table')) for x in lock_tables]
                options = {'table_list': (' ').join(table_list)}
                customized_warn_scanner(warn, p, database, False, options)
