create schema if not exists clubot_bd;
set search_path = clubot_bd, public;

drop table if exists users cascade;
create table users (
    id serial primary key,
    username varchar(255) not null,
    mentor bool not null,
    info text
);

drop table if exists club cascade;
create table club (
    id serial primary key,
    name varchar(255) not null,
    info text
);

drop table if exists club_x_user cascade;
create table club_x_user (
    id serial primary key,
    club_id integer not null,
    user_id integer not null,
    role varchar(255) not null,
    info text,
    foreign key (club_id) references club(id),
    foreign key (user_id) references users(id)
);

drop table if exists event cascade;
create table event (
    id serial primary key,
    club_id integer not null,
    host_id integer not null,
    info text,
    foreign key (club_id) references club(id),
    foreign key (host_id) references users(id)
);

drop table if exists event_reg cascade;
create table event_reg (
    id serial primary key,
    user_id integer not null,
    event_id integer not null,
    info text,
    foreign key (user_id) references users(id),
    foreign key (event_id) references event(id)
);

drop table if exists mentorship cascade;
create table mentorship (
    id serial primary key,
    mentor_id integer not null,
    mentee_id integer not null,
    club_id integer not null,
    info text,
    foreign key (mentor_id) references users(id),
    foreign key (mentee_id) references users(id),
    foreign key (club_id) references club(id)
);

drop table if exists achievement cascade;
create table achievement (
    id serial primary key,
    info text
);

drop table if exists user_x_achievement cascade;
create table user_x_achievement (
    id serial primary key,
    user_id integer not null,
    achievement_id integer not null,
    info text,
    foreign key (user_id) references users(id),
    foreign key (achievement_id) references achievement(id)
);

drop table if exists questionnaire cascade;
create table questionnaire (
    id serial primary key,
    user_id integer not null,
    info text,
    foreign key (user_id) references users(id)
);

drop table if exists randomcoffee cascade;
create table randomcoffee (
    id serial primary key,
    user_id1 integer not null,
    user_id2 integer not null,
    club_id integer not null,
    info text,
    foreign key (user_id1) references users(id),
    foreign key (user_id2) references users(id),
    foreign key (club_id) references club(id)
);
