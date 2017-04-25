d3.select("ul.maList")
  .style("visibility", "hidden");

function button() {
  var ul = d3.select("a#Analysis");
  ul
    .on("mouseover", expand);

    function expand(d) {
      d3.select("ul.maList")
        .style("opacity", .9)
        .style("visibility", "unset");
    }//Expand

  var listicles = d3.select("div#errythingElse");
  listicles
  .on("mouseover", hide);

  function hide(d) {
    d3.select("ul.maList")
      .style("visibility", "hidden");
  }//Hide
}//Button
button();
