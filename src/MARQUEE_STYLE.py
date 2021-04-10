import re
import sys
# Marquee CSS Style

MARQUEE_STYLE = re.sub("(\r\n|\n|\r)", "", """
marquee {
  font-size: 20px;
  transition: all .4s;
  margin: 10px 5px;
}

.marquee {
  position: relative;
  overflow: hidden;
  --move-initial: 120vw;
  --move-final: -100%;
}

.marquee[data-direction="right"] {
  --move-initial: -100%;
  --move-final: 200vw;
}

.marquee-content {
  width: fit-content;
  display: flex;
  position: relative;
  transform: translate3d(var(--move-initial), 0, 0);
  animation: marquee 15s linear infinite;
  animation-play-state: running;
}

@keyframes marquee {
  0% {
    transform: translate3d(var(--move-initial), 0, 0);
  }
  100% {
    transform: translate3d(var(--move-final), 0, 0);
  }
}""")

sys.modules[__name__] = MARQUEE_STYLE