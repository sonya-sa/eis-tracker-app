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
    console.log(project['eis id']);

    // twitter button with custome text to include project details
    projectDisplayElInnerHtml += '<a class="twitter-share-button" href="https://twitter.com/intent/tweet?text=' + 'There is a new project open for public comment' + ' : ' + 'EIS ID:' + project["eis id"] + '.' + 'Make your voice heard! Submit a comment by: '+ project["Comment due date"] + '"> Tweet</a>';
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
    center: {lat: 47.5515, lng: -101.0020},
    zoom: 3,
    gestureHandling: 'cooperative',
    styles: [{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#7f2200"},{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"visibility":"on"},{"color":"#87ae79"}]},{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#495421"}]},{"featureType":"administrative","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"},{"visibility":"on"},{"weight":4.1}]},{"featureType":"administrative.neighborhood","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"geometry.fill","stylers":[{"color":"#abce83"}]},{"featureType":"poi","elementType":"geometry.fill","stylers":[{"color":"#769E72"}]},{"featureType":"poi","elementType":"labels.text.fill","stylers":[{"color":"#7B8758"}]},{"featureType":"poi","elementType":"labels.text.stroke","stylers":[{"color":"#EBF4A4"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"visibility":"simplified"},{"color":"#8dab68"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#5B5B3F"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ABCE83"}]},{"featureType":"road","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#EBF4A4"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"weight":"0.56"}]},{"featureType":"road.highway.controlled_access","elementType":"geometry.stroke","stylers":[{"weight":"0.50"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#d8d385"}]},{"featureType":"road.arterial","elementType":"geometry.stroke","stylers":[{"weight":"0.18"},{"lightness":"21"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#A4C67D"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"geometry","stylers":[{"visibility":"on"},{"color":"#aee2e0"}]}]

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

      google.maps.event.addListener(marker,'click',function() {
  map.setZoom(4);
  map.setCenter(marker.getPosition());
  });
    }
}

function initMap() {
  $.get('/states_with_projects.json', displayMap);
}
