
from django.urls import path
from .views import User_views
from .views import work_management_views
from .views import job_views
from .views import progress_views

#prueba

urlpatterns = [
    
    #Genericas usuarios

    path('users', User_views.UserList.as_view(), name = 'user-list' ),

    path('users/<int:pk>' , User_views.UserDetail.as_view(), name = 'user-detail' ),
    #originales usuarios

    path('user/login', User_views.user_login, name='user_login'),

    path('users/deactivate/<int:pk>' , User_views.user_deactivate, name = 'user_deactivate' ),

    # obtener por rol (NEW)

    path('users/get_gerentes/' , User_views.user_get_gerente, name = 'user_gerentes' ),

    path('users/get_peones/' , User_views.user_get_peones, name = 'user_peones' ),

    path('users/get_capataces/' , User_views.user_get_capataces, name = 'user_capataces' ),

    path('users/get_directores/' , User_views.user_get_directores, name = 'user_capataces' ),

    path('users/get_ayudantes/' , User_views.user_get_ayudantes, name = 'user_capataces' ),


    
    
    # URL para la gestión de obra

    path('work-management/', work_management_views.WorkManagementList.as_view(), name='work-management-list'),
    
    path('work-management/<int:pk>/', 
         work_management_views.WorkManagementDetail.as_view(), name='work-management-detail'),

    path('work-management/task/<int:obra_id>/', 
         work_management_views.tasks_by_work_management, name='tasks_by_work_management'),

    path('work-management/acepted_task/<int:obra_id>/',
          work_management_views.accepted_tasks_by_work_management, name='accepted_tasks_by_work_management'),

    path('work-management/percentage_task/<int:obra_id>/',
          work_management_views.percentage_accepted_tasks_by_work_management, 
          name='accepted_tasks_by_work_management'),

     # URL para la gestión de tareas

    path('job-management/', job_views.JobManagementList.as_view(), name='work-management-list'),

    path('job-management/<int:pk>/', 
         job_views.JobManagementDetail.as_view(), name='work-management-detail'),

    path('job_management/<int:obra_id>/tasks',
         job_views.tasks_by_work_management, name='tasks-by-work-management'),
          
     # URL para la gestión de avances 

    path('progress/', progress_views.ProgressManagementList.as_view(), name='progress-list'),

    path('progress/<int:pk>/', progress_views.ProgressManagementDetail.as_view(), name='progress-detail'),
     




]