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

  var listicles = d3.select("img");

  listicles
  .on("mouseover", hide);

  function hide(d) {
    d3.select("ul.maList")
      .style("opacity", 0);
  }

}



button();
