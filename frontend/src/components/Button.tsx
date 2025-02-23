interface ButtonProps {
    onClick: () => void;
    color?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark';
    content: string;
}

const Button = ({onClick, color = 'primary', content}: ButtonProps) => {


    return <button type="button" className={"btn btn-" + color} onClick={onClick}>{content}</button>
}

export default Button