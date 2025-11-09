create table tb_address_info
(
    id           bigint auto_increment comment '编号'
        primary key,
    parent_id    bigint      not null comment '父级编号',
    name         varchar(64) not null comment '位置名称',
    address_type char        not null comment '类型',
    image_info   varchar(5012) null comment '图片',
    file_info    varchar(5012) null comment '文件',
    remark       text        not null comment '备注',
    status       char        not null comment '状态',
    user_id      bigint      not null comment '创建人',
    create_time  datetime    not null comment '创建时间',
    update_time  datetime null comment '更新时间'
) comment '位置表' row_format = DYNAMIC;

create table tb_schedule_info
(
    id          bigint auto_increment comment '编号'
        primary key,
    name        varchar(255) not null comment '名称',
    peoples     int          not null comment '人数',
    file        varchar(2550) null comment '文件',
    image       varchar(2550) null comment '图片',
    status      char         not null comment '状态',
    remark      text null comment '备注',
    user_id     bigint       not null comment '创建人',
    create_time datetime     not null comment '创建时间',
    update_time datetime null comment '更新时间'
) comment '课程表' row_format = DYNAMIC;

