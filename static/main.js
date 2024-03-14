function search() {
    let input, filter;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    cards = document.getElementsByClassName("card")
    titles = document.getElementsByClassName("card-title");

    for (i = 0; i < cards.length; i++) {
      a = titles[i];
      if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
        cards[i].style.display = "";
      } else {
        cards[i].style.display = "none";
      }
    }
}

function getRuntime(){
    const myElement = document.getElementById("movie-cards");
    let index = 1;

    for (const child of myElement.children) {
      let data =  JSON.parse(document.getElementById(`movie-data-${index}`).innerHTML)

       function toHoursAndMinutes(totalMinutes) {
          const hours = Math.floor(totalMinutes / 60);
          const minutes = totalMinutes % 60;
          return `${hours}h${minutes > 0 ? ` ${minutes}m` : ""}`;
        }
      if (data.Runtime){
        document.getElementById(`card-runtime-text-${index}`).innerHTML =
        ` ${toHoursAndMinutes(data.Runtime.split("min")[0])} <br/> <i>
        Ends at

        ${new Date( Date.now() + data.Runtime.split("min")[0]*60*1000 ).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })} </i>`

       }
      index++
    }
}
