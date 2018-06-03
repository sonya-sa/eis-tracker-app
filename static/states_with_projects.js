      let states_with_projects;
      function showProjectDataForState(state_id) {

        console.log(states_with_projects);
        const state_dict = states_with_projects[state_id]
        const projects = state_dict.projects;

        const projectDisplayEl = document.querySelector('.projectData');

        let projectDisplayElInnerHtml = '';
        for (let project of projects) {
          console.log(project);
          projectDisplayElInnerHtml += `<h2>Project: ${project.title}</h2>`;
          
          for (let property in project) {
             projectDisplayElInnerHtml += '<div>' + property + ': ' + project[property] + '</div>';
          }

          // twitter button with custome text to include project details
          projectDisplayElInnerHtml += '<a class="twitter-share-button" href="https://twitter.com/intent/tweet?text=' + '@' + project.agency + ' , ' + 'EIS ID:' + project.eis_id + '"> Tweet</a>';
          //projectDisplayElInnerHtml += '<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="my custom text"' +
          // ' data-show-count="false">Tweet</a>'
          projectDisplayElInnerHtml += ' ' + '<a class="fb-share-button" data-href="https://developers.facebook.com/docs/plugins/" data-layout="button" data-size="small" data-mobile-iframe="true"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fplugins%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Share</a></a>'; 

        }

        projectDisplayEl.innerHTML = projectDisplayElInnerHtml;
      }

    function displayMap(results) {
      states_with_projects = results;
      console.log(states_with_projects);
      const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.8283, lng: -98.5795},
        zoom: 3
      });

        for (let state_id of Object.keys(states_with_projects)) {
          let state_dict = states_with_projects[state_id];

          if (state_dict.projects.length <= 0) {
            continue
          }

          const marker = new google.maps.Marker({
              position: {lat: state_dict.geo_lat, lng: state_dict.geo_long},
              title: 'EIS Tracker',
              map: map,
              label: String(state_dict.projects.length),
            });

          marker.addListener('click', function() {
              showProjectDataForState(state_id);
          });
        }


      // console.log('state_project_map: ' + JSON.stringify(state_project_map));
    }

    function initMap() {
      $.get('/states_with_projects.json', displayMap);
    }
