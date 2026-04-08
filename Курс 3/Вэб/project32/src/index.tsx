import { createRoot } from "react-dom/client";
import "./styles.css";

const domNode = document.getElementById("root") as HTMLDivElement;
const root = createRoot(domNode);
root.render(
  <>
    <p>
      Привет, меня зовут <span className="name">Проша</span>!
    </p>
    <p>
      Скоро я стану крутым <span className="profession">frontend-разработчиком</span>!
    </p>
  </>
);