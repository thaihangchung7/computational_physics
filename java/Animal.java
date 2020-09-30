// Single Line comments
/*
  Multi-line comments
*/

import java.util.Scanner;
import java.util.*;

public class Animal { // public: "Anyone can access it"

  public static final double FAVNUMBER = 3.14159; /*
                                                   * static: "# will be shared with every animal object created" final:
                                                   * "# is a constant and cannot be changed (Common to define them with all caps)"
                                                   */

  // variables and fields fields are attributes for whatever we are defining
  // private: only can be accessed by other methods in a class
  private String name;
  private int weight;
  private boolean hasOwner = false;
  private byte age;
  private long uniqueID;
  private char favoriteChar;
  private double speed;
  private float height;

  //protected datatype: value can only be accessed by other code in the package
  //"It wouldnt make sense for a dog to know the total number of animal objects created"
  protected static int numberOfAnimals = 0;


  /*
  Scanner: allows user input from the keyboard
  System.in: takes data from keyboard
  constructor
  */
  static Scanner userInput = new Scanner(System.in);
  //constructor: "everytime an animal is created, you need a function called a constructor to be executed" 
  public Animal() {
    //dog.java extends Animal, cat.java extends Animal hence, "super class" is Animals
    //super();
    numberOfAnimals++;

    int sumOfNumbers = 5 +1;
    System.out.println("5 + 1 = " + sumOfNumbers);

    System.out.print("Enter the name: \n");

      if(userInput.hasNextLine()){
        this.setName(userInput.nextLine());
      }
  }

  public static void main (String[] args) {
    Animal theAnimal = new Animal();
  }

}
