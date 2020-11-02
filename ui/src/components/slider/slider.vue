<template>
  <Row :gutter="20">
    <i-col span="4" style="float:left;">
      <Button class="slider-btn" @click="wordChange(-1)"> 
          <Icon size="30px" type="ios-arrow-back"></Icon>      
        </Button>

      </i-col>
    <i-col span="16" style="margin:0 auto; text-align: center;">
      <a class="carousel-word">{{value}}</a>
    </i-col>
    <i-col span="4" style="float:right;">
      <Button class="slider-btn" @click="wordChange(1)"> 
          <Icon size="30px" type="ios-arrow-forward" ></Icon>
        </Button>
    </i-col>
  </Row>
</template>

<script>
export default {
  name: 'Sliders',
  props: {
    value: String
  },
  methods: {
    wordChange(pos) {
      // let dicts = ['a','b','c','d','e','f','g','h','i','j','k']
      if (pos === 1) {
        this.$emit('watchChild','1')
      } else {
        this.$emit('watchChild','0')
      }
    }
  },
  computed: {
    styles () {
      return {
        fontSize: `${this.size}px`,
        color: this.color
      }
    }
  }
}
</script>

<style lang="less" scoped>
.slider-btn {
  border: none;
  background-color: transparent;
  outline: 0;
  :active {
    outline:none;
  }
  :focus{
    outline: 0;
  }
}
.carousel-word {
}
</style>
