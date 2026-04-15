import { createRoot } from "react-dom/client";
import "./styles.css";

let name = "Проша";
let profession = "frontend-разработчиком";
const domNode = document.getElementById("root") as HTMLDivElement;
const root = createRoot(domNode);
root.render(
  <>
    <p>
      Привет, меня зовут <span className="name">{name}</span>!
    </p>
    <p>
      Скоро я стану крутым <span className="profession">{profession}</span>!
    </p>
  </>
);