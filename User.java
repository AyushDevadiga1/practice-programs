class User{
    String name;
    int age;
    public User(String name,int age){
        this.name=name;
        this.age=age;
        }
    public void Say(){
        System.out.println("My name is : "+age);
        }
    public void Gender(String gender){
        System.out.println("I am a "+gender);
        }
    }
class Human extends User{
    String name;
    int age;
    
    public Human(String name,int age){
        this.name=name;
        this.age=age;
        }
    }
public class New{
    public static void main(String[] Args)
{
    User u = new User("Ambrose",18);
     u.Say();
     u.Gender("Male");
     Human h = new Human("Neville",20);
     h.say();
    }
}
