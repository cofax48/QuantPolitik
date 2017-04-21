d3.select("ul.maList")
  .style("opacity", 0);


function button() {
  var ul = d3.select("a#Analysis");

  ul
    .on("mouseover", expand);


    function expand(d) {
      d3.select("ul.maList")
        .style("opacity", .9);
    }

  var listicles = d3.select("div#errythingElse");
  listicles
  .on("mouseover", hide);

/*
  var first = d3.select("section#first");
  first
  .on("mouseover", hide);
  var two = d3.select("section#zero");
  two
  .on("mouseover", hide);
  var three = d3.select("section#three");
  three
  .on("mouseover", hide);
  var four = d3.select("section#four");
  four
  .on("mouseover", hide);
  var five = d3.select("section#five");
  five
  .on("mouseover", hide);

*/
  function hide(d) {
    console.log("yayyyyyy");
    d3.select("ul.maList")
      .style("opacity", 0);
  }

}



button();
