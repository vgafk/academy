const { request, gql } = require('graphql-request')

const number_in_left_list = 0

exports.index = function (req, res){
    // res.render('students_list', {groups: ['group_name']})

    const query = gql`
        query{
          faculties{
            name
            groups{
              id
              name
              study_year
            }
           }
        }
    `
    request('http://localhost:4000/', query).then((data) => {
        res.render('pages/students_index',
            {current_link_number: number_in_left_list,
            facultys_list :data['faculties'],
            title: "Список студентов"})
    })
}